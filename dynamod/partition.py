from dynamod.core import *
from dynamod.afterdist import *

class Partition:
    """a class describing population partition by successively specifying property values"""

    def __init__(self, model, share=1, given={}, slices=None, after=None, tbefore=None):
        self.model = model
        self.share = share
        self.given = given
        self.after = after
        self.slices = slices
        self.slicekey = None
        self.afterdist = None
        self.tbefore = tbefore

    def initialize(self):
        if self.slices is None:
            self.slices = [NOSLICE for att in self.model.attSystem.attributes]

    def has_segment(self, axis, value):
        current = self.get_axis(axis)
        if isinstance(current, list):
            return value in current
        return value == current

    def get_axis(self, axis):
        try:
            return self.given[axis]
        except KeyError:
            raise MissingAxis(axis)

    def restricted(self, axis, value):
        try:
            att = self.model.attSystem.attr_map[axis]
            slices = self.slices.copy()
            if isinstance(value, list):
                value_indices = [att.values.index(v) for v in value]
                slices[att.index] = tuple(value_indices)
            else:
                value_index = att.values.index(value)
                slices[att.index] = value_index
        except ValueError:
            raise ConfigurationError("illegal attribute comparision of " + axis + " with " + value)
        given = self.given.copy()
        given[axis] = value
        return Partition(self.model, self.share, given, slices, self.after, self.tbefore)

    def with_prob(self, prob):
        return Partition(self.model, self.share * prob, self.given, self.slices, self.after, self.tbefore)

    def with_after(self, op:DynamodAfter):
        return Partition(self.model, self.share, self.given, self.slices, op, self.tbefore)

    def before(self, tbefore):
        if isinstance(tbefore, int):
            return Partition(self.model, self.share, self.given, self.slices, self.after, tbefore)
        raise ConfigurationError("argument of .tbefore() must be int")

    def segment(self):
        return tuple(self.slices)

    def segkey(self):
        if self.slicekey is None:
            self.slicekey = deslice(self.slices)
        return self.slicekey

    def get_shape(self):
        shape = []
        for att in self.model.attSystem.attributes:
            if self.slicekey[att.index] is None:
                shape.append(len(att.values))
        return tuple(shape)

    def srckey(self):
        return None if self.after is None else self.after.key

    def describe(self):
        text = (str(self.share) + " of ") if self.share != 1 else ""
        if len(self.given) == 0:
            text += "ALL"
        else:
            text += str(self.given)
        if self.after is not None:
            text += " after " + self.after.distrib
        if self.tbefore is not None:
            text += " tbefore " + self.tbefore
        return text

    def transfer(self):
        if self.after is None:
            if self.tbefore is None or self.tbefore > self.model.tick:
                return self.share * self.model.matrix[self.segment()]
            return self.share * self.model.history.matrix[self.model.tick - self.tbefore][self.segment()]
        if self.afterdist is None:
            self.afterdist = AfterDistribution.get_distribution(self.model, self, self.after)
        return self.share * self.afterdist.get_share()

    def total(self):
        return self.transfer().sum()
