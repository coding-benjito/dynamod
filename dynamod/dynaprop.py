from dynamod.core import *


class DynaModel:
    def __init__(self, desc: DynamodDesc):
        self.parameters = ParameterSystem(desc.params)
        self.properties = PropertySystem(self, desc.properties)
        self.population = self.buildMatrix()


class ParameterSystem:
    def __init__(self, pardefs: dict):
        self.params = {}
        if pardefs is not None:
            for n, v in pardefs.items():
                if isinstance(v, int) or isinstance(v, float):
                    self.params[n] = v
                else:
                    raise ConfigurationError("parameter '" + n + "' must be defined as a number")


class PropertySystem:
    """holds all properties"""

    def __init__(self, model:DynaModel, props: dict[str, DynamodProp]):
        self.model = model
        self.properties = []
        self.prop_map = {}
        for n, p in props.items():
            self.add_property(Property(n, p))

    def add_property(self, prop):
        prop.index = len(self.properties)
        self.properties.append(prop)
        self.prop_map[prop.name] = prop

class Property:
    """one property used to partition a group"""

    def __init__(self, name: str, dp: DynamodProp):
        self.index = 0
        self.name = name
        self.values = dp.values
        self.value_map = {}
        for v in dp.values:
            self.value_map[v] = self.values.index(v)
        self.shares = ShareSystem (self, dp.shares)

class ShareSystem:
    def __init__(self, prop:Property, shares):
        self.prop = prop
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

class ConditionalShares:
    def __init__(self, prop:Property, condshare):
        self.axis = condshare[0][0]
        self.value = condshare[0][1]
        self.share = ShareSystem(prop, condshare[1])

class ShareValue:
    def __init__(self, prop: Property, value):
        if isinstance(value, DynamodElseList):
            self.share_list = [ConditionalShareValue(prop, s) for s in value.list]
            if (value.otherwise is not None):
                self.share_otherwise = ShareValue(prop, value.otherwise)
        else:
            self.value = value

class ConditionalShareValue:
    def __init__(self, prop:Property, condshare):
        self.axis = condshare[0][0]
        self.value = condshare[0][1]
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

