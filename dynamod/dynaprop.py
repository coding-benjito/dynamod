from dynamod.core import *
import json

class DynaModel:
    def __init__(self, desc: DynamodDesc):
        self.tick = 0
        self.parameters = ParameterSystem(desc.params)
        self.properties = PropertySystem(self, desc.properties)
        self.population = []
        self.matrix = self.properties.build_matrix()

    def hasParam (self, name):
        return self.parameters.knows(name)

    def getParam (self, name):
        return self.parameters.get(name)

    def getSysParam (self, name):
        if name == 'time' or name == 'day':
            return self.tick;
        if name == 'Population' or name == 'ALL':
            return self.partition
        return None

    def invokeFunc(self, funcname, args):
        pass


class ParameterSystem:
    def __init__(self, pardefs: dict):
        self.params = {}
        if pardefs is not None:
            for n, v in pardefs.items():
                if is_num(v):
                    self.params[n] = v
                else:
                    raise ConfigurationError("parameter '" + n + "' must be defined as a number")

    def knows (self, key):
        return key in self.params

    def get (self, key):
        return self.params[key]

class PropertySystem:
    """holds all properties"""

    def __init__(self, model:DynaModel, props: dict[str, DynamodProp]):
        self.model = model
        self.properties = []
        self.prop_map = {}
        for n, p in props.items():
            self.add_property(Property(model, n, p))

    def add_property(self, prop):
        prop.index = len(self.properties)
        if prop.index != 0:
            self.properties[-1].next = prop
        self.properties.append(prop)
        self.prop_map[prop.name] = prop

    def build_matrix(self):
        given = {}
        return self.properties[0].build_matrix (given, 1)



class Property:
    """one property used to partition a group"""

    def __init__(self, model: DynaModel, name: str, dp: DynamodProp):
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
    def __init__(self, prop:Property, shares):
        self.prop = prop
        self.share_list = None
        self.share_otherwise = None
        self.share_map = None
        if isinstance(shares, list):
            if len(shares) != len(prop.values):
                raise ConfigurationError("share list has wrong number of entries for property " + prop.name)
            self.share_map = {}
            for v,s in zip(prop.values, shares):
                self.share_map[v] = ShareValue(prop, s)
        elif isinstance(shares, dict):
            self.share_map = {}
            for v,s in shares.items():
                self.share_map[v] = ShareValue(prop, s)
        elif isinstance(shares, DynamodElseList):
            self.share_list = [ConditionalShares(prop, s) for s in shares.list]
            if (shares.otherwise is not None):
                self.share_otherwise = ShareSystem(prop, shares.otherwise)
        else:
            raise ConfigurationError("unrecognized share system for property " + prop.name)

    def build_shares (self, given:dict[str,str]):
        if self.share_list is None:
            array = []
            for ax in self.prop.values:
                if ax not in self.share_map:
                    raise ConfigurationError("value '" + ax + "' of property '" + self.prop.name + "' has no defined share")
                array.append(self.share_map[ax].build_share (ax, given))
            return self.normalize(array)
        for sl in self.share_list:
            if sl.matches(given):
                return sl.share.build_shares (given)
        if self.share_otherwise is None:
            raise ConfigurationError("no matching for-condition while evaluation shares for " + self.prop.name + " in context " + json.dumps(given))
        return self.share_otherwise.build_shares(given)

    def normalize(self, array):
        total = 0.0
        rest_at = None
        i = 0
        for s in array:
            if s == -1 and rest_at is None:
                rest_at = i
            elif s < 0:
                raise ConfigurationError("inconsistent shares for property " + self.prop.name)
            else:
                total += s
            i += 1
        if rest_at is not None:
            array[rest_at] = 1.0 - total
            return array
        if total == 0:
            raise ConfigurationError("zero shares for property " + self.prop.name)
        elif total < 0.999999 or total > 1.000001:
            raise ConfigurationError("shares for property " + self.prop.name + " don't add up to 1")
        return [a/total for a in array]


class ConditionalShares:
    def __init__(self, prop:Property, condshare):
        self.prop = prop
        if isinstance(condshare[0], DynamodAxisValue):
            self.axis = condshare[0].axis
            self.value = condshare[0].value
        else:
            raise ConfigurationError("property shares can only be switches by axis values")
        self.share = ShareSystem(prop, condshare[1])

    def matches (self, given:dict[str,str]):
        if not self.axis in given:
            raise ConfigurationError("axis '" + self.axis + "' not defined while evaluating shares of '" + self.prop.name +"'")
        if isinstance(self.value, list):
            return given[self.axis] in self.value
        return given[self.axis] == self.value

class ShareValue:
    def __init__(self, prop: Property, value):
        self.prop = prop
        self.share_list = None
        self.share_otherwise = None
        self.value = None
        if isinstance(value, DynamodElseList):
            self.share_list = [ConditionalShareValue(prop, s) for s in value.list]
            if (value.otherwise is not None):
                self.share_otherwise = ShareValue(prop, value.otherwise)
        else:
            self.value = value

    def build_share (self, axvalue:str, given:dict[str,str]):
        from dynamod.evaluation import evalExpr
        if self.share_list is None:
            return evalExpr (self.prop.model, self.value, given=given)
        for sl in self.share_list:
            if sl.matches(given):
                return sl.share.build_share (axvalue, given)
        if self.share_otherwise is None:
            raise ConfigurationError("no matching for-condition while evaluation share'" + axvalue + "' for " + self.prop.name)
        return self.share_otherwise.build_share (axvalue, given)


class ConditionalShareValue(ConditionalShares):
    def __init__(self, prop:Property, condshare):
        self.prop = prop
        if isinstance(condshare[0], DynamodAxisValue):
            self.axis = condshare[0].axis
            self.value = condshare[0].value
        else:
            raise ConfigurationError("property share can only be switches by axis values", condshare.ctx)
        self.share = ShareValue(prop, condshare[1])

class Partition:
    """a class describing population partition by successively specifying property values"""

    def __init__(self, base, value, share, axis):
        self.base = base
        self.value = value
        self.share = share
        self.axis = axis



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
