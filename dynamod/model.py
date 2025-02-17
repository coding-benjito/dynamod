from dynamod.evaluation import *
from dynamod.actionstack import *
from dynamod.checks import *
from dynamod.tracer import Tracer
from dynamod.partition import Partition
from dynamod.history import History
from collections import OrderedDict
import json
import numpy as np
import random

class DynaModel:
    def __init__(self, srcfile):
        self.srcfile = srcfile
        self.formulas = {}
        self.functions = {}
        self.parameters = {}
        self.userObjects = {}
        self.results = {}
        self.progressions = OrderedDict()
        self.autosplits = {}
        self.attDescs = OrderedDict()
        self.trace = False
        self.check = False
        self.trace_for = None
        self.raw_errors = False
        self.simulate = False
        self.ctx_stack = []
        self.error_stack = None
        self.tracer = None
        self.builtin = BuiltinFunctions(self)

    def initialize(self, parameters=None, objects=None):
        try:
            with Action(self, "initializing model", line=False):
                if parameters is not None:
                    self.parameters.update(parameters)
                if objects is not None:
                    self.userObjects.update(objects)
                self.baseStore = self.build_basestore()
                self.attSystem = AttributeSystem(self)
                self.context = DynaContext(self, Segop(self))
                for name, attDesc in self.attDescs.items():
                    self.attSystem.addAttribute(name, attDesc)
                self.context.onseg = Segop(self)
                self.all_none = [None for att in self.attSystem.attributes]
                self.matrix = np.array(self.attSystem.build_matrix())
                self.incoming = np.zeros_like(self.matrix)
                self.outgoing = np.zeros_like(self.matrix)
                self.tick = 0
                self.distributions = {}
                self.history = History(self)
                self.history.store()
                self.simulate = True
                self.step()
                self.simulate = False

        except Exception as e:
            if self.raw_errors:
                raise e from None
            report_actions(self, e)
            exit(1)

    def evalExpr (self, expr, onseg=None):
        if onseg is not None:
            self.context.onseg = onseg
        return evalExpression(expr, self.context)

    def evalCond(self, expr, onseg=None):
        if onseg is not None:
            self.context.onseg = onseg
        return evalCondition(expr, self.context)

    def tprint(self, *text):
        if self.trace:
            print (*text)

    def include(self, path):
        keep = self.srcfile
        self.srcfile = path
        parse_model(path, self)
        self.srcfile = keep

    def trace_on(self, map, split_by=None):
        self.trace_for = tuple([att.indexof(map[att.name]) if att.name in map else NOSLICE for att in self.attSystem.attributes])
        self.trace_split = None
        if split_by is not None:
            self.trace_split = 0
            for  att in self.attSystem.attributes:
                if att.name == split_by:
                    break;
                if att.name not in map:
                    self.trace_split += 1
        self.trace_val = self.get_traceval(self.matrix)

    def get_traceval(self, of):
        if self.trace_for is None:
            return None
        res = of[self.trace_for]
        if self.trace_split is None:
            return res.sum()
        return res.sum(self.trace_split)

    def attribute(self, axis):
        try:
            return self.attSystem.attr_map[axis]
        except ValueError:
            raise ConfigurationError("unknown attribute '" + axis + "'")
        
    def indexof (self, axis, value):
        att = self.attribute(axis)
        try:
            return (att.index, att.indexof(value))
        except ValueError:
            raise ConfigurationError("unknown value '" + value + "' for attribute'" + axis + "'")

    def attindex (self, axis, value):
        att = self.attribute(axis)
        try:
            return (att, att.indexof(value))
        except ValueError:
            raise ConfigurationError("unknown value '" + value + "' for attribute'" + axis + "'")

    def run(self, cycles, trace_at=None):
        for i in range(cycles):
            if i == trace_at:
                self.tracer = Tracer()
            self.step()
            if i == trace_at:
                self.tracer.finish()
                self.tracer = None

    def step(self):
        try:
            with Action(self, "progressions for tick " + str(self.tick), line=False):
                self._step()
        except MissingAxis:
            self.tprint("retry step", self.tick)
            self.trace_val = self.get_traceval(self.matrix)
            self.matrix = self.backup.copy()
            self.step()
        except Exception as e:
            if self.raw_errors:
                raise e from None
            report_actions(self, e)
            exit(1)

    def _step(self):
        self.init_step()
        for name, prog in self.progressions.items():
            with Action(self, "perform progression " + name, line=False):
                self.enter_local_context()
                if self.tracer is not None:
                    self.tracer.line("perform " + name)
                self.tprint("perform", name)
                try:
                    onsegs = self.perform_autosplit_steps (prog, name)
                    if not self.simulate:
                        self.apply_changes (onsegs)
                except MissingAxis as miss_axis:
                    raise miss_axis
                finally:
                    self.leave_local_context()
        if not self.simulate:
            self.close_step()

    def perform_autosplit_steps (self, prog, name):
        if name in self.autosplits:
            splits = self.autosplits[name]
        else:
            splits = []
        try:
            return self.perform_split_steps(prog, Segop(self), splits.copy())
        except MissingAxis as miss_axis:
            splits.append(miss_axis.axis)
            self.tprint("add axis", miss_axis, "to", name)
            self.autosplits[name] = splits
            raise miss_axis

    def perform_split_steps (self, prog, onseg:Segop, splits):
        if len(splits) == 0:
            self.baseStore.clear_cache()
            return self.perform_steps(prog, onseg)
        axis = splits.pop()
        att = self.attribute(axis)
        onsegs = []
        for seg in onseg.split_on_axis(att.index):
            onsegs.extend(self.perform_split_steps(prog, seg, splits.copy()))
        return onsegs


    def enter_local_context(self):
        self.context.values = self.context.values.extended()

    def leave_local_context(self):
        self.context.values = self.context.values.base

    def init_step(self):
        self.baseStore.clear_cache()
        self.backup = self.matrix.copy()

    def close_step(self):
        #print('.', end='')
        self.tickover()
        if self.check:
            check_correctness(self)
        if self.trace_for is not None:
            check_tickchange(self, self.tick)
        self.history.store()

    def tickover(self):
        for adist in self.distributions.values():
            adist.tickover()
        self.tick += 1

    def perform_steps(self, steps, onseg:Segop, alias=None):
        if self.tracer is not None:
            self.tracer.begin("operate on " + onseg.desc())
        if alias is not None:
            self.context.values.put(alias, Partition(self, onseg))
        onsegs = [onseg]
        for step in steps:
            nextsegs = []
            for seg in onsegs:
                nextsegs.extend (self.perform_step(step, seg))
            onsegs = nextsegs
        if self.tracer is not None:
            self.tracer.end()
        return onsegs

    def perform_step(self, op, onseg:Segop):
        with Action(self, op=op):
            if isinstance(op, DynamodElseList):
                return self.perform_restrictions(op, onseg)
            elif isinstance(op, DynamodAfter):
                return self.perform_after (op, onseg)
            elif isinstance(op, DynamodAction):
                return self.perform_action (op, onseg)
            elif isinstance(op, DynamodVarDef):
                self.perform_vardef (op, onseg)
                return [onseg]
            else:
                raise ConfigurationError("unknown progression operarion: " + op, op.ctx)

    def perform_action (self, op:DynamodAction, onseg: Segop):
        att = self.attribute(op.axis)
        if isinstance(op.state, str):
            ivalue = att.indexof(op.state)
            if onseg.needs_split(att.index, ivalue):
                onsegs = onseg.split_on_att(att.index, ivalue)
                onsegs[1].set_value(att.index, ivalue)
                return onsegs
            onseg.set_value(att.index, ivalue)
            return [onseg]
        elif isinstance(op.state, dict):
            shares = {}
            for state, share in op.state.items():
                shares[att.indexof(state)] = self.evalExpr(share, onseg)
            normalize_map(shares, op.axis, op.ctx)
            return onseg.split_by_shares(att.index, shares)
        else:
            raise ConfigurationError("unknown state description: " + op.state, op.ctx)

    def apply_changes(self, onsegs):
        for seg in onsegs:
            if seg.change != self.all_none:
                self.apply_change(seg)
        self.matrix += (self.incoming - self.outgoing)
        self.incoming = np.zeros_like(self.matrix)
        self.outgoing = np.zeros_like(self.matrix)
        if self.check:
            check_total(self)
            check_nonnegatives(self)


    def apply_change(self, onseg):
        key = onseg.as_key()
        for sout, sin in onseg.to_apply():
            transfer = onseg.share * self.matrix[sout]
            if self.trace and self.trace_for is None:
                self.tprint(str(onseg) + ": " + str(transfer.sum()))

            self.outgoing[sout] += transfer
            self.incoming[sin] += transfer

            for adist in self.distributions.values():
                adist.distribute(sin, sout, transfer, key)
        if self.check:
            check_total(self)
            check_nonnegatives(self)

    def calc_after_share(self, op, onseg):
        after = AfterDistribution.get_distribution(self, op, onseg.seg)
        return after.get_share()

    def perform_after (self, op:DynamodAfter, onseg):
        with Action(self, "perform after", op=op):
            prob = self.calc_after_share(op, onseg)
            both = onseg.split_on_prob(prob)
            onsegs = self.perform_steps(op.block, both[0])
            onsegs.append(both[1])
        return onsegs

    def perform_vardef (self, op:DynamodVarDef, onseg:Segop):
        self.context.values.put(op.varname, self.evalExpr(op.expression, onseg))

    def perform_restrictions (self, op:DynamodElseList, onseg):
        onsegs = []
        axes = set()
        axvalues = set()
        for restr in op.list:
            with Action(self, "perform conditional", op=restr):
                if restr.type == 'if':
                    is_true = self.evalCond(restr.cond, onseg)
                    if not is_true:
                        continue
                    return self.perform_steps (restr.block, onseg, restr.alias)
                elif isinstance(restr.cond, DynamodAxisValue):
                    axval = restr.cond
                    axes.add(axval.axis)
                    att = self.attribute(axval.axis)
                    if len(axes) > 1:
                        raise ConfigurationError("sequence of for-conditions must use same attribute")
                    value = axval.value
                    if isinstance(value, list):
                        axvalues.update(value)
                        for v in value:
                            ivalue = att.indexof(v)
                            if not onseg.needs_split(att.index, ivalue):
                                raise ConfigurationError("redundant or contradictive for-condition")
                            both = onseg.split_on_att(att.index, ivalue)
                            onsegs.extend (self.perform_steps(restr.block, both[0], restr.alias))
                            onseg = both[1]
                    else:
                        value = self.evalExpr(value, onseg)
                        axvalues.add(value)
                        ivalue = att.indexof(value)
                        if onseg.needs_split(att.index, ivalue):
                            both = onseg.split_on_att(att.index, ivalue)
                            onsegs.extend (self.perform_steps(restr.block, both[0], restr.alias))
                            onseg = both[1]
                        elif onseg.has_value(att.index, ivalue):
                            onsegs.extend (self.perform_steps(restr.block, onseg, restr.alias))

                else:
                    if len(axes) > 0:
                        raise ConfigurationError("cannot combine attribute and probability conditions")
                    if len(onsegs) > 0:
                        raise ConfigurationError("cannot chain probability conditions, must use 'otherwise'")
                    prob = self.evalExpr(restr.cond, onseg)
                    both = onseg.split_on_prob(prob)
                    onsegs = self.perform_steps(restr.block, both[0])
                    if op.otherwise is None:
                        onsegs.append(both[1])
                    else:
                        onsegs.extend (self.perform_steps (op.otherwise, both[1]))
                    return onsegs

        if op.otherwise is not None:
            axis = axes.pop()
            others = set(self.attribute(axis).values) - axvalues
            for v in others:
                ivalue = att.indexof(v)
                if not onseg.needs_split(att.index, ivalue):
                    raise ConfigurationError("redundant or contradictive otherwise")
                both = onseg.split_on_att(att.index, ivalue)
                onsegs.extend (self.perform_steps(op.otherwise, both[0]))
                onseg = both[1]
        else:
            onsegs.append (onseg)
        return onsegs

    def invokeFunc(self, funcname, args):
        if self.tracer is not None:
            key = funcname + "("
            if args is not None:
                key += ", ".join(str(arg) for arg in args)
            key += ")"
            self.tracer.begin(key)
        if funcname not in self.functions:
            if hasattr(self.builtin, funcname):
                method = getattr(self.builtin, funcname)
                if callable(method):
                    res = method(*args)
            raise EvaluationError("unknown function: " + funcname)
        else:
            res = self.functions[funcname].evaluate (args, self.context)
        if self.tracer is not None:
            self.tracer.end(res)
        return res

    def build_basestore(self):
        store = GlobalStore(self)
        store = store.extendedBy(ImmutableMapStore(self.parameters))
        store = store.extendedBy(FormulaStore(self))
        store = store.extendedBy(ImmutableMapStore(self.userObjects))
        return store

    def addParameter (self, ctx, name, expr):
        if is_num(expr):
            self.parameters[name] = expr
        else:
            raise ConfigurationError("parameter '" + name + "' must be defined as a number")

    def addResult (self, ctx, name, expr):
        self.results[name] = DynamodExpression(self, ctx, name, expr)

    def addProgression (self, ctx, name, progressions:list, before=None):
        if before is not None:
            self.progressions = insert_at(self.progressions, name, progressions, before)
        else:
            self.progressions[name] = progressions

    def addFormula(self, ctx, name, expr):
        self.formulas[name] = DynamodExpression(self, ctx, name, expr)

    def addFunc(self, ctx, name, args, expr):
        self.functions[name] = DynamodFunction(self, ctx, name, args, expr)

    def addAttribute(self, ctx, name, attdesc:DynamodAttrib):
        self.attDescs[name] = attdesc

    def full_partition(self):
        return Partition(self)

    def get_attribute(self, axis, value, start=None, stop=None):
        return self.history.get_attribute(axis, value, start, stop)

    def get_attributes(self, axis, start=None, stop=None):
        return self.history.get_attributes(axis, start, stop)

    def get_result(self, name, start=None, stop=None):
        return self.history.get_result(name, start, stop)

    def get_results(self, names, start=None, stop=None):
        return self.history.get_results(names, start, stop)

    def get_all_results(self, start=None, stop=None):
        return self.history.get_all_results(start, stop)

class AttributeSystem:
    """holds all properties"""

    def __init__(self, model:DynaModel):
        self.model = model
        self.attributes = []
        self.attr_map = {}

    def addAttribute(self, name:str, att:DynamodAttrib):
        att = Attribute(self.model, name, att)
        att.index = len(self.attributes)
        if att.index != 0:
            self.attributes[-1].next = att
        self.attributes.append(att)
        self.attr_map[att.name] = att

    def build_matrix(self):
        given = {}
        return self.attributes[0].build_matrix (given, 1)



class Attribute:
    """one attribute used to partition a group"""

    def __init__(self, model: DynaModel, name: str, dp: DynamodAttrib):
        self.model = model
        self.index = 0
        self.next = None
        self.name = name
        self.values = dp.values
        self.value_map = {}
        for v in dp.values:
            self.value_map[v] = self.indexof(v)
        self.shares = ShareSystem (self, dp.shares)

    def indexof (self, value):
        try:
            return self.values.index(value)
        except ValueError:
            raise ConfigurationError("unknown value '" + value + "' for attribute'" + self.name + "'")

    def build_shares (self, given:dict[str,str]):
        return self.shares.build_shares (given)

    def build_matrix (self, given:dict[str,str], base):
        matrix = []
        quota = self.build_shares(given)
        i = 0
        for s in quota:
            entry = s * base
            if self.next is None:
                matrix.append(entry)
            else:
                given[self.name] = self.values[i]
                matrix.append(self.next.build_matrix (given, entry))
            i += 1
        return matrix

    def normalize_list(self, array, ctx=None):
        return normalize_list(array, self.name, ctx)

    def normalize_map(self, shares, ctx=None):
        normalize_map(shares, self.name, ctx)

class ShareSystem:
    def __init__(self, att:Attribute, shares):
        self.att = att
        self.share_list = None
        self.share_otherwise = None
        self.share_map = None
        if isinstance(shares, list):
            if len(shares) != len(att.values):
                raise ConfigurationError("share list has wrong number of entries for attribute " + att.name)
            self.share_map = {}
            for v,s in zip(att.values, shares):
                self.share_map[v] = ShareValue(att, s)
        elif isinstance(shares, dict):
            self.share_map = {}
            for v,s in shares.items():
                self.share_map[v] = ShareValue(att, s)
        elif isinstance(shares, DynamodElseList):
            self.share_list = [ConditionalShares(att, s) for s in shares.list]
            if (shares.otherwise is not None):
                self.share_otherwise = ShareSystem(att, shares.otherwise)
        else:
            raise ConfigurationError("unrecognized share system for attribute " + att.name)

    def build_shares (self, given:dict[str,str]):
        if self.share_list is None:
            array = []
            for ax in self.att.values:
                if ax not in self.share_map:
                    raise ConfigurationError("value '" + ax + "' of attribute '" + self.att.name + "' has no defined share")
                array.append(self.share_map[ax].build_share (ax, given))
            return self.att.normalize_list(array)
        for sl in self.share_list:
            if sl.matches(given):
                return sl.share.build_shares (given)
        if self.share_otherwise is None:
            raise ConfigurationError("no matching for-condition while evaluation shares for " + self.att.name + " in context " + json.dumps(given))
        return self.share_otherwise.build_shares(given)


class ConditionalShares:
    def __init__(self, att:Attribute, condshare):
        self.att = att
        if isinstance(condshare[0], DynamodAxisValue):
            self.axis = condshare[0].axis
            self.value = condshare[0].value
        else:
            raise ConfigurationError("attribute shares can only be switches by axis values")
        self.share = ShareSystem(att, condshare[1])

    def matches (self, given:dict[str,str]):
        if not self.axis in given:
            raise ConfigurationError("attribute value for '" + self.axis + "' not defined while evaluating shares of '" + self.att.name + "'")
        if isinstance(self.value, list):
            return given[self.axis] in self.value
        return given[self.axis] == self.value

class ShareValue:
    def __init__(self, att: Attribute, value):
        self.att = att
        self.share_list = None
        self.share_otherwise = None
        self.value = None
        if isinstance(value, DynamodElseList):
            self.share_list = [ConditionalShareValue(att, s) for s in value.list]
            if (value.otherwise is not None):
                self.share_otherwise = ShareValue(att, value.otherwise)
        else:
            self.value = value

    def build_share (self, axvalue:str, given:dict[str,str]):
        if self.share_list is None:
            return self.att.model.evalExpr (self.value)
        for sl in self.share_list:
            if sl.matches(given):
                return sl.share.build_share (axvalue, given)
        if self.share_otherwise is None:
            raise ConfigurationError("no matching for-condition while evaluation share'" + axvalue + "' for " + self.att.name)
        return self.share_otherwise.build_share (axvalue, given)


class ConditionalShareValue(ConditionalShares):
    def __init__(self, att:Attribute, condshare):
        self.att = att
        if isinstance(condshare.cond, DynamodAxisValue):
            self.axis = condshare.cond.axis
            self.value = condshare.cond.value
        else:
            raise ConfigurationError("attribute share can only be switches by axis values", condshare.ctx)
        self.share = ShareValue(att, condshare.expr)

class GlobalStore(ImmutableMapStore):
    def __init__(self, model):
        self.model = model
        self.here = {'ALL': self.all, 'day': self.tick, 'time': self.tick, 'random': self.random}

    def get(self, key):
        if key in self.here:
            return self.here[key]()

    def all(self):
        return self.model.full_partition()

    def current(self):
        return self.model.context.segop

    def tick(self):
        return self.model.tick

    def random(self):
        return random.random()

class BuiltinFunctions:
    def __init__(self, model):
        self.model = model

    def min(self, *args):
        return min(*args)

    def max(self, *args):
        return max(*args)

    def abs(self, x):
        return abs(x)

    def ceil(self, x):
        return math.ceil(x)

    def floor(self, x):
        return math.floor(x)

    def round(self, x):
        return round(x)

class FormulaStore(ImmutableMapStore):
    def __init__(self, model):
        self.model = model
        self.here = model.formulas
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        self.cache[key] = 0
        expr = self.here[key]
        if self.model.tracer is not None:
            self.model.tracer.begin (key)
        res = self.model.evalExpr(expr)
        if self.model.tracer is not None:
            self.model.tracer.end (res)
        self.cache[key] = res
        return res

    def clear_cache(self):
        self.cache = {}

def parse_model (srcfile:str, model=None, trace=False):
    from antlr4 import FileStream, CommonTokenStream
    from dynamod.parser.DynamodLexer import DynamodLexer
    from dynamod.parser.DynamodParser import DynamodParser
    from dynamod.builder import DynamodBuilder
    from dynamod.parse_helper import RegisterErrorListener

    input = FileStream(srcfile)
    lexer = DynamodLexer(input)
    stream = CommonTokenStream(lexer)
    parser = DynamodParser(stream)
    listener = RegisterErrorListener()
    parser.addErrorListener(listener);
    parser.setTrace(trace)
    tree = parser.model()
    if listener.had_error:
        print("processing terminated due to syntax errors in " + srcfile)
        exit(1)
    if model is None:
        model = DynaModel(srcfile)
    builder = DynamodBuilder(model)
    builder.visitModel(tree)
    return model

def get_total(matrix):
    if isinstance(matrix, list):
        return sum([get_total(s) for s in matrix])
    return matrix

def normalize_list(array, name="?", ctx=None):
    total = 0.0
    rest_at = None
    i = 0
    for s in array:
        if s == -1 and rest_at is None:
            rest_at = i
        elif s < 0:
            raise ConfigurationError("inconsistent shares for attribute " + name, ctx)
        else:
            total += s
        i += 1
    if rest_at is not None:
        array[rest_at] = 1.0 - total
        return array
    if total == 0:
        raise ConfigurationError("zero shares for attribute " + name, ctx)
    elif total < 0.999999 or total > 1.000001:
        raise ConfigurationError("shares for attribute " + name + " don't add up to 1", ctx)
    return [a/total for a in array]

def normalize_map(shares, name="?", ctx=None):
    total = 0.0
    rest_val = None
    for v, s in shares.items():
        if s == -1 and rest_val is None:
            rest_val = v
        elif s < 0:
            raise ConfigurationError("inconsistent shares for property " + name, ctx)
        else:
            total += s
    if rest_val is not None:
        shares[rest_val] = 1.0 - total
    elif total == 0:
        raise ConfigurationError("zero shares for property " + name, ctx)
    elif total < 0.9999 or total > 1.0001:
        raise ConfigurationError("shares for property " + name + " don't add up to 1", ctx)
    else:
        for v, s in shares.items():
            shares[v] = s / total

