from gradescent import *
from dynamod.model import DynaModel
from dynamod.core import *
from statistics import *
import numpy as np
from numpy.polynomial import Polynomial

def minpos (xdata, ydata):
    poly = Polynomial.fit(xdata, ydata, deg=2)
    s = poly.deriv()
    x = s.roots()[0]
    return x, poly(x)
class Calibration:
    def __init__(self, model:DynaModel, cycles):
        self.model = model
        self.cycles = cycles
        self.targets = []
        self.parameters = []

    def add_target(self, resultname, expected, type='values', start=0, stop=None, weight=1, metric='mean_absolute_error'):
        self.targets.append (Target (self.model, resultname, expected, type=type, start=start, stop=stop, weight=weight, metric=metric))

    def add_variable(self, name, min=None, max=None, grid=None, integral=False, dx=None):
        initial_value = None
        if grid is None:
            initial_value = self.model.parameters[name]
        par = Parameter(name, initial_value, min=None, max=None, grid=None, integral=False, dx=None)
        self.parameters.append(par)

    def optimize(self, zoom_limit=1e6, momentum=0, iterations=100, min_improvement=0.0001, trace=True, debug=False):
        np.seterr(all='raise')
        optimizer = Optimizer(self.get_error, args='dict', zoom_limit=zoom_limit, cfactor=0.5, momentum=momentum, iterations=iterations, min_improvement=min_improvement, trace=trace, debug=debug)
        for par in self.parameters:
            optimizer.add_par(par)
        return optimizer.optimize()

    def get_error(self, params):
        self.model.initialize(params)
        self.model.run(self.cycles)
        return sum(target.get_error() for target in self.targets)

class Target:
    def __init__(self, model:DynaModel, resultname, expected, type='values', start=0, stop=None, weight=1, metric='mean_absolute_error'):
        self.model = model
        self.resultname = resultname
        self.expected = expected
        self.type = type
        self.start = start
        self.stop = stop
        self.weight = weight
        self.metric = metric

    def get_error(self):
        result = self.model.get_result(self.resultname, self.start, self.stop)
        if self.type == 'values':
            if isinstance(self.expected, list) or isinstance(self.expected, tuple):
                expected = self.expected
            else:
                try:
                    expected = [x for x in self.expected]
                except TypeError:
                    expected = [self.expected for _ in result]
            if len(result) != len(expected):
                raise ConfigurationError("number of expected values mismatch on result " + self.resultname)
        else:
            result = [self.get_minmax_point (result)]
            expected = [self.expected]
        try:
            method = getattr(self, self.metric)
            return self.weight * method(result, expected)
        except Exception as e:
            raise ConfigurationError("error invoking metric " + self.metric) from e

    def get_minmax_point(self, values):
        find_min = self.type == 'min' or self.type == 'tmin'
        find_arg = self.type == 'tmin' or self.type == 'tmax'
        pos = np.argmin(values) if find_min else np.argmax(values)
        if pos == 0 or pos == len(values) - 1:
            return pos if find_arg else values[pos]
        poly = Polynomial.fit([pos-1, pos, pos+1], [values[pos-1], values[pos], values[pos+1]], deg=2)
        s = poly.deriv()
        x = s.roots()[0]
        return x if find_arg else poly(x)

    def mean_absolute_error(self, calced, expected):
        return mean([abs(x - y) for x, y in zip(calced, expected)])

    def mean_squared_error(self, calced, expected):
        return mean([(x - y)**2 for x, y in zip(calced, expected)])

    def max_absolute_error(self, calced, expected):
        return max([abs(x - y) for x, y in zip(calced, expected)])

    def median_absolute_error(self, calced, expected):
        return median([abs(x - y) for x, y in zip(calced, expected)])

