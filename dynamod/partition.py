from dynamod.core import *

class Partition:
    """a class describing population partition by successively specifying property values"""

    def __init__(self, model, share=1, given={}, slices=None):
        self.model = model
        self.share = share
        self.given = given
        self.slices = slices

    def initialize(self):
        if self.slices is None:
            self.slices = [slice(None) for att in self.model.attSystem.attributes]

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
        return Partition(self.model, self.share, given, slices)

    def with_prob(self, prob):
        return Partition(self.model, self.share * prob, self.given, self.slices)

    def segment(self, dim=None, index=None):
        slices = self.slices.copy()
        if dim is not None:
            slices[dim] = index
        return tuple(slices)

    def describe(self, share=None):
        if share is None:
            share = self.share
        text = (str(share) + " of ") if self.share != 1 else ""
        if len(self.given) == 0:
            text += "ALL"
        else:
            text += str(self.given)
        return text

    def total(self):
        return self.model.matrix[self.segment()].sum()
