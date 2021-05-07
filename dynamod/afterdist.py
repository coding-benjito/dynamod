from dynamod.core import *
import math

class AfterDistribution:
    distributions = {}

    def get_distribution (model, op:DynamodAfter):
        if op.key in AfterDistribution.distributions:
            return AfterDistribution.distributions[op.key]
        dist = AfterDistribution (model, op)
        AfterDistribution.distributions[op.key] = dist
        return dist

    def __init__(self, model, op:DynamodAfter):
        self.model = model
        self.partition = model.context.partition
        methodname = "after_" + op.distrib
        if not hasattr(AfterDistribution, methodname):
            raise ConfigurationError("unknown after-distribution " + op.distrib, op.ctx)
        try:
            if op.args is None:
                self.timeshares = getattr(AfterDistribution, methodname)()
            else:
                args = [model.evalExpr(arg) for arg in op.args]
                self.timeshares = getattr(AfterDistribution, methodname)(*args)
        except Exception as e:
            raise ConfigurationError("error invoking after-distribution " + op.distrib + ": " + str(e.args), op.ctx)

    def after_fix(delay):
        if delay <= 0:
            raise ValueError("after.fix delay must be positive")
        if delay < 1:
            delay = 1
        len = math.ceil(delay)
        timeshares = [0 for i in range(len)]
        timeshares[-1] = delay - len
        rest = 1 + len - delay
        if rest > 0:
            timeshares[-2] = rest
        return timeshares

    def after_explicit(*args):
        from dynaprop import normalize_list
        return normalize_list(*args, name="after.explicit attributes")

