import numpy as np

from dynamod.core import *
from scipy.stats import norm
import math

class AfterDistribution:
    distributions = {}

    def get_distribution (model, partition, op:DynamodAfter):
        argvals = [model.evalExpr(arg) for arg in op.args]
        key = (partition.segkey(), op.distrib, tuple(argvals))
        if key in AfterDistribution.distributions:
            return AfterDistribution.distributions[key]
        dist = AfterDistribution (model, partition, op)
        AfterDistribution.distributions[key] = dist
        return dist

    def __init__(self, model, partition, op:DynamodAfter):
        self.model = model
        self.dist = op.distrib
        self.distmethod = "after_" + op.distrib
        if not hasattr(AfterDistribution, self.distmethod):
            raise ConfigurationError("unknown after-distrbution " + op.distrib, op.ctx)
        self.argvals = [model.evalExpr(arg) for arg in op.args]
        self.key = (partition.segkey(), op.distrib, tuple(self.argvals))
        self.timeshares = self.get_timeshares()
        self.segment = partition.segment()
        self.shape = partition.get_shape()
        full = model.matrix[self.segment]
        self.sections = [x * full for x in self.timeshares]
        self.incoming = np.zeros(self.shape)
        self.outgoing = np.zeros(self.shape)
        if model.check:
            self.check()

    def reset(self):
        self.incoming = np.zeros(self.shape)
        self.outgoing = np.zeros(self.shape)

    def calc_rfactor (self, timeshares):
        r = 0
        for i in range(len(timeshares)):
            r += (i+1) * timeshares[i]
        return 1 / r

    def get_timeshares(self):
        try:
            return getattr(AfterDistribution, self.distmethod)(*self.argvals)
        except Exception as e:
            raise ConfigurationError("error invoking distribution " + self.distmethod + ": " + str(e.args))

    def get_share(self):
        return self.sections[0]

    def describe(self):
        return "after." + self.dist

    def apply (self):
        self.sections.pop(0)
        self.sections.append (np.zeros(self.shape))
        for i in range(len(self.timeshares)):
            self.sections[i] += self.timeshares[i] * self.incoming
        f = np.zeros(self.shape)
        all = sum(self.sections)
        np.divide(all - self.outgoing, all, out=f, where=all>0)
        for i in range(len(self.timeshares)):
            self.sections[i] *= f
        self.incoming = np.zeros(self.shape)
        self.outgoing = np.zeros(self.shape)

    def check(self):
        res = self.model.matrix[self.segment].copy()
        for section in self.sections:
            res -= section
        if np.amin(res) < -0.00000001:
            raise EvaluationError("after-distribution corrupted")

    @staticmethod
    def after_fix(delay):
        if delay <= 0:
            raise ValueError("after.fix delay must be positive")
        if delay < 1:
            delay = 1
        len = math.ceil(delay)
        timeshares = [0 for i in range(len)]
        if len > delay:
            timeshares[-1] = len - delay
            rest = 1 + delay - len
            timeshares[-2] = rest
        else:
            timeshares[-1] = 1
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

    @staticmethod
    def distribute_transfer(sin, sout, transfer, srckey):
        for adist in AfterDistribution.distributions.values():
            if adist.key == srckey:
                continue
            mysin, tr_sub, my_sub = intersect(sin, adist.segment)
            if mysin is not None:
                adist.incoming[my_sub] += transfer[tr_sub]
            mysout, tr_sub, my_sub = intersect(sout, adist.segment)
            if mysout is not None:
                adist.outgoing[my_sub] += transfer[tr_sub]

    @staticmethod
    def apply_afters():
        for adist in AfterDistribution.distributions.values():
            adist.apply()

    @staticmethod
    def apply_checks():
        for adist in AfterDistribution.distributions.values():
            adist.check()

    @staticmethod
    def reset_all():
        for adist in AfterDistribution.distributions.values():
            adist.reset()
