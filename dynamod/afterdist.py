from dynamod.core import *
from scipy.stats import norm
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
        self.key = op.key
        self.dist = op.distrib
        self.distmethod = "after_" + op.distrib
        if not hasattr(AfterDistribution, self.distmethod):
            raise ConfigurationError("unknown after-distrbution " + op.distrib, op.ctx)
        self.args = op.args
        timeshares = self.get_timeshares()
        self.rfactor = self.calc_rfactor (timeshares)

    def calc_rfactor (self, timeshares):
        r = 0
        for i in range(len(timeshares)):
            r += (i+1) * timeshares[i]
        return 1 / r

    def get_timeshares(self):
        try:
            argvals = [self.model.evalExpr(arg) for arg in self.args]
            return getattr(AfterDistribution, self.distmethod)(*argvals)
        except Exception as e:
            raise ConfigurationError("error invoking distribution " + self.distmethod + ": " + str(e.args))

    def get_share(self, segment):
        timeshares = self.get_timeshares()
        share = 0
        for i in range(len(timeshares)):
            share += timeshares[i] * self.model.history.get_incoming(segment, self.model.tick - i, self.rfactor)
        return share

    def describe(self):
        return "after." + self.dist

    @staticmethod
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

    @staticmethod
    def after_explicit(*args):
        from dynaprop import normalize_list
        return normalize_list(*args, name="after.explicit attributes")


    @staticmethod
    def after_std (loc=0, scale=1):
        cdf = norm(loc, scale).cdf
        shares = []
        total = 0
        upper = 1.5
        lower = None
        while total < 0.999:
            share = cdf(upper)
            if lower is not None:
                share -= cdf(lower)
            total += share
            shares.append (share)
            upper += 1
            lower = upper - 1
        shares[-1] += 1 - total
        return shares