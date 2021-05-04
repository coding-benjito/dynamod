from dynamod.core import *
from dynamod.evaluation import *
import json

class DynaModel:
    def __init__(self, srcfile):
        self.srcfile = srcfile
        self.parameters = {}
        self.formulas = {}
        self.functions = {}
        self.parameters = {}
        self.results = {}
        self.progressions = {}
        self.baseStore = self.build_basestore()
        self.partition = Partition(self)
        self.context = DynaContext(self)
        self.attributes = AttributeSystem(self)
        self.matrix = self.attributes.build_matrix()
        self.tick = 0

    def invokeFunc(self, funcname, args):
        pass

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
        self.functions[name] = DynamodFunction(self, ctx, args, name, expr)

    def addAttribute(self, ctx, name, attdesc:DynamodAttrib):
        self.attributes.addAttribute(name, attdesc)


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
            return self.normalize(array)
        for sl in self.share_list:
            if sl.matches(given):
                return sl.share.build_shares (given)
        if self.share_otherwise is None:
            raise ConfigurationError("no matching for-condition while evaluation shares for " + self.att.name + " in context " + json.dumps(given))
        return self.share_otherwise.build_shares(given)

    def normalize(self, array):
        total = 0.0
        rest_at = None
        i = 0
        for s in array:
            if s == -1 and rest_at is None:
                rest_at = i
            elif s < 0:
                raise ConfigurationError("inconsistent shares for attribute " + self.att.name)
            else:
                total += s
            i += 1
        if rest_at is not None:
            array[rest_at] = 1.0 - total
            return array
        if total == 0:
            raise ConfigurationError("zero shares for attribute " + self.att.name)
        elif total < 0.999999 or total > 1.000001:
            raise ConfigurationError("shares for attribute " + self.att.name + " don't add up to 1")
        return [a/total for a in array]


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
        from dynamod.evaluation import evalExpr
        if self.share_list is None:
            return evalExpr (self.value, self.att.model.context)
        for sl in self.share_list:
            if sl.matches(given):
                return sl.share.build_share (axvalue, given)
        if self.share_otherwise is None:
            raise ConfigurationError("no matching for-condition while evaluation share'" + axvalue + "' for " + self.att.name)
        return self.share_otherwise.build_share (axvalue, given)


class ConditionalShareValue(ConditionalShares):
    def __init__(self, att:Attribute, condshare):
        self.att = att
        if isinstance(condshare[0], DynamodAxisValue):
            self.axis = condshare[0].axis
            self.value = condshare[0].value
        else:
            raise ConfigurationError("attribute share can only be switches by axis values", condshare.ctx)
        self.share = ShareValue(att, condshare[1])

class Partition:
    """a class describing population partition by successively specifying property values"""

    def __init__(self, model, share=1, given:dict=[]):
        self.model = model
        self.share = share
        self.given = given

    def normalize(self, share_result):
        total = 0.0
        rest_val = None
        for v, s in share_result.items:
            if s == -1 and rest_val is None:
                rest_val = v
            elif s < 0:
                raise ConfigurationError("inconsistent shares for property " + self.axis.name)
            else:
                total += s
        if rest_val is not None:
            share_result[rest_val] = 1.0 - total
        elif total == 0:
            raise ConfigurationError("zero shares for property " + self.axis.name)
        elif total < 0.9999 or total > 1.0001:
            raise ConfigurationError("shares for property " + self.axis.name + " don't add up to 1")
        else:
            for v, s in share_result.items:
                share_result[v] = s / total

class GlobalStore(ImmutableMapStore):
    def __init__(self, model):
        self.model = model
        self.here = {'ALL': self.all, 'day': self.tick, 'time': self.tick}

    def get(self, key):
        if key in self.here:
            method = getattr(self, self.here[key])
            return method()

    def all(self):
        return Partition(self.model)

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
        res = evalExpr(expr, self.model.context)
        self.cache[key] = res
        return res

    def clear_cache(self):
        self.cache = {}
