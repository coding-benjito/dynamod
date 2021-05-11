from dynamod.core import *
import pandas as pd

class History:
    def __init__(self, model):
        self.model = model
        self.matrix = []
        self.results = {}
        for name in self.model.results:
            self.results[name] = []

    def store(self):
        self.matrix.append(self.model.matrix.copy())
        for name, expr in self.model.results.items():
            self.results[name].append (self.model.evalExpr(expr))

    def get_attribute(self, axis, value, start=0):
        segment = axval_segment(self.model, axis, value)
        return [m[segment].sum() for m in self.matrix[start:]]

    def get_attributes(self, axis, start=0):
        att = self.model.attSystem.attr_map[axis]
        axl = axis_exclude(self.model, axis)
        data = [m.sum(axis=axl) for m in self.matrix[start:]]
        return pd.DataFrame(data, columns=att.values)

    def get_result(self, name, start=0):
        pass
    def get_results(self, start=0):
        pass
    def all_results(self, start=0):
        pass
