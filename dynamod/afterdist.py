import numpy as np

from dynamod.core import *
from scipy.stats import norm
import math

class AfterDistribution:
    distributions = {}

    def get_distribution (model, partition, op:DynamodAfter):
        argvals = [model.evalExpr(arg) for arg in op.args]
        key = (partition.segkey(), get_line(op.ctx), tuple(argvals))
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
        self.key = (partition.segkey(), get_line(op.ctx), tuple(self.argvals))
        self.timeshares = self.get_timeshares()
        self.segment = partition.segment()
        self.shape = partition.get_shape()
        self.init_sections()
        self.leftover = np.zeros(self.shape)
        self.current_batch = None
        self.taken_out = None
        if model.check:
            self.check()

    def calc_rfactor (self, timeshares):
        r = 0
        for i in range(len(timeshares)):
            r += (i+1) * timeshares[i]
        return 1 / r

    def init_sections(self):
        full = self.model.matrix[self.segment]
        flow = full * self.calc_rfactor(self.timeshares)
        #build [xn, xn-1+xn, ... x1+x2+...+xn]
        factors = np.cumsum(self.timeshares[::-1])[::-1]
        self.sections = [x * flow for x in factors]

    def get_timeshares(self):
        try:
            return getattr(AfterDistribution, self.distmethod)(*self.argvals)
        except Exception as e:
            raise ConfigurationError("error invoking distribution " + self.distmethod + ": " + str(e.args))

    def assert_current(self):
        if self.current_batch is None:
            self.normalize()
            self.current_batch = self.sections[0]
            self.sections[0] = np.zeros(self.shape)
            self.taken_out = np.zeros(self.shape)

    def get_share(self):
        if self.model.simulate:
            return self.sections[0]
        self.assert_current()
        return self.current_batch

    def normalize(self):
        f = np.zeros(self.shape)
        all = sum(self.sections) + self.leftover
        full = self.model.matrix[self.segment]
        np.divide(full, all, out=f, where=all>0)
        for i in range(len(self.timeshares)):
            self.sections[i] *= f
        self.leftover *= f

    def describe(self):
        return "after." + self.dist

    def distribute (self, sin, sout, transfer, srckey):
        if self.key == srckey:
            self.assert_current()
            self.taken_out += transfer
            return
        ssin, tr_sin, my_sin = intersect(sin, self.segment)
        ssout, tr_sout, my_sout = intersect(sout, self.segment)
        if ssout is None and ssin is not None:
            incoming = transfer[tr_sin]
            if len(my_sin) == 0:
                for i in range(len(self.timeshares)):
                    self.sections[i] += self.timeshares[i] * incoming
            else:
                for i in range(len(self.timeshares)):
                    self.sections[i][my_sin] += self.timeshares[i] * incoming

    def tickover (self):
        self.assert_current()
        self.leftover += self.current_batch - self.taken_out
        self.current_batch = None
        self.taken_out = None
        self.sections[0] += self.sections[1]
        self.sections.pop(1)
        self.sections.append (np.zeros(self.shape))

    def check(self):
        return
        res = self.model.matrix[self.segment].copy()
        for section in self.sections:
            res -= section
        res -= self.leftover
        if np.amin(res) < -0.00000001:
            raise EvaluationError("after-distribution corrupted")

    @staticmethod
    def after_fix(delay):
        if delay <= 0:
            raise ValueError("after.fix delay must be positive")
        if delay < 1:
            delay = 1
        len = math.ceil(delay)
        timeshares = [0 for i in range(len+1)]
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
        upper = 0.5
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
            adist.distribute (sin, sout, transfer, srckey)

    @staticmethod
    def apply_afters():
        for adist in AfterDistribution.distributions.values():
            adist.apply()

    @staticmethod
    def apply_checks():
        for adist in AfterDistribution.distributions.values():
            adist.check()

    @staticmethod
    def tickover_all():
        for adist in AfterDistribution.distributions.values():
            adist.tickover()
