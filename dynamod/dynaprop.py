from core import *

class PartitionAxis:
    """one property used to partition a group"""
    def __init__(self, name, values, prevAxis):
        self.name = name
        self.values = values
        self.prev = prevAxis
        self.next = None
        if prevAxis is not None:
            prevAxis.next = self

class Partition:
    """a class describing population partition by successively specifying property values"""
    def __init__(self, base, value, share, axis):
        self.base = base
        self.value = value
        self.share = share
        self.axis = axis

class ShareGetter:
    """abstract class to retrieve a single share in a context"""
    def get_share(self, context: dict, axis: PartitionAxis, axis_value: str) -> float:
        raise Exception ("get_share called on abstract base class")

class SharesGetter:
    """abstract class to retrieve the shares of a whole axis in a context"""
    def get_shares(self, context: dict[PartitionAxis, str], axis: PartitionAxis) -> dict:
        raise Exception ("get_shares called on abstract base class")

class SharesMap(SharesGetter):
    def __init__(self, axis: PartitionAxis, shares: dict):
        self.axis = axis
        self.shares = shares
        self.normalize()

    def enumerated(cls, axis: PartitionAxis, share_list: list[float]):
        if len(share_list) > len(axis.values):
            raise ConfigurationError("too many share values for " + axis.name)
        if len(share_list) < len(axis.values):
            raise ConfigurationError("not enough share values for " + axis.name)
        shares = {}
        i = 0
        for v in axis.values:
            shares[v] = share_list[i]
            i += 1
        return cls(axis, shares)

    def normalize(self, share_result):
        total = 0.0
        rest_val = None
        for v,s in share_result:
            if s == -1 and rest_val is None:
                rest_val = v
            elif s < 0:
                raise ConfigurationError ("inconsistent shares for property " + self.axis.name)
            else:
                total += s
        if rest_val is not None:
            share_result[rest_val] = 1.0 - total
        elif total == 0:
            raise ConfigurationError("zero shares for property " + self.axis.name)
        elif total < 0.9999 or total > 1.0001:
            raise ConfigurationError("shares for property " + self.axis.name + " don't add up to 1")
        else:
            for v, s in share_result:
                share_result[v] = s / total

    def get_shares(self, context: dict[PartitionAxis, str]) -> dict[str, float]:
        share_result = {}
        for v,s in self.shares:
            if isinstance(s, float) or isinstance(s, int):
                share_result[v] = s
            elif  isinstance(s, ShareGetter):
                share_result[v] = s.get_share(self.context, self.axis, v)
        self.normalize(share_result)
        return share_result
