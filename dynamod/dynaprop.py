from dynamod.core import *
from dynamod.evaluation import *
from dynamod.actionstack import *
from dynamod.afterdist import *
from dynamod.partition import Partition
from collections import OrderedDict
import json
import numpy as np

class DynaModel:
    def __init__(self, srcfile):
        self.srcfile = srcfile
        self.parameters = {}
        self.formulas = {}
        self.functions = {}
        self.parameters = {}
        self.results = {}
        self.progressions = {}
        self.autosplits = {}
        self.attDescs = OrderedDict()
        self.trace = False
        self.ctx_stack = []

    def initialize(self):
        try:
            with Action("initializing model", line=False):
                self.baseStore = self.build_basestore()
                self.context = DynaContext(self, Partition(self))
                self.attSystem = AttributeSystem(self)
                for name, attDesc in self.attDescs.items():
                    self.attSystem.addAttribute(name, attDesc)
                self.context.partition.initialize()
                self.matrix = np.array(self.attSystem.build_matrix())
                self.tick = 0
        except Exception as e:
            report_actions(e)
            exit(1)

    def evalExpr (self, expr):
        return evalExpression(expr, self.context)

    def evalCond(self, expr):
        return evalCondition(expr, self.context)

    def tprint(self, *text):
        print (*text)

    def include(self, path):
        keep = self.srcfile
        self.srcfile = path
        parse_model(path, self)
        self.srcfile = keep

    def step(self):
        try:
            with Action("progressions for tick " + str(self.tick), line=False):
                self._step()
        except MissingAxis:
            if self.trace:
                self.tprint("retry step", self.tick)
            self.step()
        except Exception as e:
            report_actions(e)
            exit(1)

    def _step(self):
        self.init_step()
        for name, prog in self.progressions.items():
            with Action("perform progression " + name, line=False):
                self.enter_local_context()
                if self.trace:
                    self.tprint("perform", name)
                try:
                    self.perform_autosplit_steps (prog, name)
                except MissingAxis as miss_axis:
                    raise miss_axis
                finally:
                    self.leave_local_context()
        self.close_step()

    def perform_autosplit_steps (self, prog, name):
        if name in self.autosplits:
            splits = self.autosplits[name]
        else:
            splits = []
        try:
            self.perform_split_steps(prog, splits.copy())
        except MissingAxis as miss_axis:
            splits.append(miss_axis.axis)
            if self.trace:
                self.tprint("add axis", miss_axis, "to", name)
            self.autosplits[name] = splits
            raise miss_axis

    def perform_split_steps (self, prog, splits):
        if len(splits) == 0:
            self.perform_steps(prog)
            return
        axis = splits.pop()
        values = self.attSystem.attr_map[axis].values
        for v in values:
            self.perform_steps_on(prog, self.context.restricted(axis, v), splits.copy())


    def enter_local_context(self):
        self.context.values = self.context.values.extended()

    def leave_local_context(self):
        self.context.values = self.context.values.base

    def init_step(self):
        self.baseStore.clear_cache()
        self.incoming = np.zeros_like(self.matrix)
        self.outgoing = np.zeros_like(self.matrix)
        if self.trace:
            self.tprint("start step", self.tick)

    def close_step(self):
        self.tick += 1
        self.matrix += (self.incoming - self.outgoing)

    def perform_steps(self, steps):
        for step in steps:
            self.perform_step(step)

    def perform_step(self, op):
        with Action(op=op):
            if isinstance(op, DynamodElseList):
                self.perform_restrictions(op)
            elif isinstance(op, DynamodAfter):
                self.perform_after (op)
            elif isinstance(op, DynamodAction):
                self.perform_action (op)
            elif isinstance(op, DynamodVarDef):
                self.perform_vardef (op)
            else:
                raise ConfigurationError("unknown progression operarion: " + op, op.ctx)

    def perform_action (self, op:DynamodAction):
        if isinstance(op.state, str):
            self.set_state(op.axis, op.state)
        elif isinstance(op.state, dict):
            shares = {}
            for state, share in op.state.items():
                shares[state] = self.evalExpr(share)
            normalize_map(shares, op.axis, op.ctx)
            for state, share in shares.items():
                self.set_state(op.axis, state, share)
        else:
            raise ConfigurationError("unknown state description: " + op.state, op.ctx)

    def perform_after (self, op:DynamodAfter):
        dist = AfterDistribution.get_distribution(self, op)
        prob = dist.get_share()
        with Action("perform after", op=op):
            self.context.push_partition(self.context.partition.with_prob(prob))
            try:
                self.perform_steps(op.block)
            finally:
                self.context.pop_partition()
        return

    def perform_vardef (self, op:DynamodVarDef):
        self.context.values.put(op.varname, self.evalExpr(op.expression))

    def perform_restrictions (self, op:DynamodElseList):
        total_prob = 1
        axes = set()
        axvalues = set()
        for restr in op.list:
            with Action("perform conditional", op=restr):
                if restr.type == 'if':
                    is_true = self.evalCond(restr.cond)
                    if not is_true:
                        continue
                    total_prob = 0
                    self.perform_on (restr, None)
                elif isinstance(restr.cond, DynamodAxisValue):
                    axval = restr.cond
                    axes.add(axval.axis)
                    value = axval.value
                    if isinstance(value, list):
                        axvalues.update(value)
                        for v in value:
                            self.perform_on (restr, self.context.restricted(axval.axis, v))
                    else:
                        value = self.evalExpr(value)
                        axvalues.add(value)
                        self.perform_on(restr, self.context.restricted(axval.axis, value))
                else:
                    prob = self.evalExpr(restr.cond)
                    total_prob -= prob
                    self.perform_on (restr, self.context.with_prob(prob))

            if op.otherwise is not None:
                if total_prob != 1:
                    if len(axes) != 0:
                        raise ConfigurationError("cannot use otherwise after mixed axis/probability restrictions", op.otherwise.ctx)
                    self.perform_on(restr, self.context.with_prob(1-total_prob))
                    return
                if len(axes) > 1:
                    raise ConfigurationError("cannot use otherwise after restrictions over multiple axes", op.otherwise.ctx)
                others = set(self.attSystem.attr_map.keys()) - axvalues
                axis = axes.pop()
                for v in others:
                    self.perform_on(restr, self.context.restricted(axis, v))

    def perform_on(self, restr:DynamodRestriction, partition):
        with Action("perform segment", op=restr):
            if restr.alias is not None:
                self.context.values.put(restr.alias, partition)
            self.context.push_partition(partition)
            try:
                self.perform_steps(restr.block)
            finally:
                self.context.pop_partition()

    def perform_steps_on(self, prog:list, partition, splits):
        self.context.push_partition(partition)
        try:
            self.perform_split_steps(prog, splits)
        finally:
            self.context.pop_partition()

    def set_state(self, axis, value, share=1):
        with Action("set " + axis + " to " + value, line=False):
            partition = self.context.partition
            att = self.attSystem.attr_map[axis]
            value_index = att.values.index(value)
            share *= partition.share
            if axis in partition.given:
                if value != partition.given[axis]:
                    sin = partition.segment(att.index, value_index)
                    sout = partition.segment()
                    transfer = share * self.matrix[sout]
                    self.tprint("in (" + partition.describe(share) + ") set " + axis + " to " + value + ": " + str(transfer.sum()))
                    self.incoming[sin] += transfer
                    self.outgoing[sout] += transfer
            else:
                for src_index in range(len(att.values)):
                    if src_index != value_index:
                        sin = partition.segment(att.index, value_index)
                        sout = partition.segment(att.index, src_index)
                        transfer = share * self.matrix[sout]
                        self.tprint("in (" + partition.restricted(axis, att.values[src_index]).describe(share) + ") set " + axis + " to " + value + ": " + str(transfer.sum()))
                        self.incoming[sin] += transfer
                        self.outgoing[sout] += transfer

    def invokeFunc(self, funcname, args):
        if funcname not in self.functions:
            raise EvaluationError("unknown function: " + funcname)
        return self.functions[funcname].evaluate (args, self.context)

    def build_basestore(self):
        return GlobalStore(self).extendedBy(ImmutableMapStore(self.parameters)).extendedBy(FormulaStore(self))

    def addParameter (self, ctx, name, expr):
        if is_num(expr):
            self.parameters[name] = expr
        else:
            raise ConfigurationError("parameter '" + name + "' must be defined as a number")

    def addResult (self, ctx, name, expr):
        self.results[name] = DynamodExpression(self, ctx, name, expr)

    def addProgression (self, ctx, name, progressions:list):
        self.progressions[name] = progressions

    def addFormula(self, ctx, name, expr):
        self.formulas[name] = DynamodExpression(self, ctx, name, expr)

    def addFunc(self, ctx, name, args, expr):
        self.functions[name] = DynamodFunction(self, ctx, name, args, expr)

    def addAttribute(self, ctx, name, attdesc:DynamodAttrib):
        self.attDescs[name] = attdesc

    def full_partition(self):
        part = Partition(self)
        part.initialize()
        return part

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
            self.value_map[v] = self.values.index(v)
        self.shares = ShareSystem (self, dp.shares)

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
        self.here = {'ALL': self.all, 'CURRENT': self.current, 'day': self.tick, 'time': self.tick}

    def get(self, key):
        if key in self.here:
            return self.here[key]()

    def all(self):
        return self.model.full_partition()

    def current(self):
        return self.model.context.partition

    def tick(self):
        return self.model.tick

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
        res = self.model.evalExpr(expr)
        self.cache[key] = res
        return res

    def clear_cache(self):
        self.cache = {}

def parse_model (srcfile:str, model=None, trace=False):
    from antlr4 import FileStream, CommonTokenStream
    from dynaparser.DynamodLexer import DynamodLexer
    from dynaparser.DynamodParser import DynamodParser
    from DynamodBuilder import DynamodBuilder

    input = FileStream(srcfile)
    lexer = DynamodLexer(input)
    stream = CommonTokenStream(lexer)
    parser = DynamodParser(stream)
    parser.setTrace(trace)
    tree = parser.model()
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

