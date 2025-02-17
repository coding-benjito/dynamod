from dynamod.afterdist import *

class Partition:
    """a class describing population partition by successively specifying property values"""

    def __init__(self, model, onseg=None, tbefore=None):
        self.model = model
        self.onseg = onseg if onseg is not None else Segop(model)
        self.tbefore = tbefore

    def restricted(self, axis, value):
        att = self.model.attribute(axis)
        if isinstance(value, list):
            ivalues = [att.indexof(v) for v in value]
            both = self.onseg.split_on_attlist(att.index, ivalues)
        else:
            both = self.onseg.split_on_att(att.index, att.indexof(value))
        return Partition(self.model, both[0], self.tbefore)

    def before(self, tbefore):
        if isinstance(tbefore, int):
            if self.tbefore is not None:
                tbefore += self.tbefore
            return Partition(self.model, self.onseg, tbefore)
        raise ConfigurationError("argument of .tbefore() must be int")

    def describe(self):
        text = str(self.onseg)
        if self.tbefore is not None:
            text += " before " + self.tbefore
        return text

    def total(self):
        if self.tbefore is None or self.tbefore > self.model.tick:
            matrix = self.model.matrix
        else:
            matrix = self.model.history.matrix[self.model.tick - self.tbefore]
        return self.onseg.share * matrix[reslice(self.onseg.seg)].sum()

    def __str__(self):
        text = self.onseg.desc()
        if self.tbefore is not None:
            text += " (before " + str(self.tbefore) + ")"
        text += " " + str(self.total())
        return text