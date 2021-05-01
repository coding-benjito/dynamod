from collections import namedtuple
from recordtype import recordtype


class ConfigurationError(Exception):
    def __init__(self, message, ctx=None, line=None, column=None):
        if ctx is not None:
            sym = None
            if hasattr(ctx, 'symbol'):
                sym = getattr(ctx, 'symbol')
            elif hasattr(ctx, 'start'):
                sym = getattr(ctx, 'start')
            if hasattr(sym, 'line'):
                line = sym.line
            if hasattr(sym, column):
                column = sym.column
        if line is not None:
            if column is not None:
                message = '[' + line + ',' + column + '] ' + message
            else:
                message = '[' + line + '] ' + message
        self.message = message

DynamodDesc = recordtype('DynamodDesc', ['basis', 'params', 'properties', 'progressions'], default=None)
DynamodProp = recordtype('DynamodProp', ['values', 'shares'])
DynamodElseList = recordtype('DynamodElseList', ['list', 'otherwise'])
DynamodVarDef = recordtype('DynamodVarDef', ['varname', 'expression'])
DynamodAfter = recordtype('DynamodAfter', ['distrib', 'args', 'block'])
DynamodAction = recordtype('DynamodAction', ['axis', 'state'])
DynamodRestriction = recordtype('DynamodRestriction', ['cond', 'block', ('alias',None)])
BinaryOp = recordtype('DualOp', ['opcode', 'op1', 'op2'])
UnaryOp = recordtype('UnaryOp', ['opcode', 'op'])

class ShareSystem:
    def share_of (self, axval:str, cube):
        pass

    def normalize(self, share_result):
        total = 0.0
        rest_val = None
        for v,s in share_result:
            if s == -1 and rest_val is None:
                rest_val = v
            elif s < 0:
                raise ConfigurationError ("inconsistent shares for property " + self.axis)
            else:
                total += s
        if rest_val is not None:
            share_result[rest_val] = 1.0 - total
        elif total == 0:
            raise ConfigurationError("zero shares for property " + self.axis)
        elif total < 0.9999 or total > 1.0001:
            raise ConfigurationError("shares for property " + self.axis + " don't add up to 1")
        else:
            for v, s in share_result:
                share_result[v] = s / total

class MappedShares(ShareSystem):
    def __init__(self, sharemap:dict):
        self.sharemap = sharemap

    def share_of(self, axval:str, cube):
        return self.sharemap[axval].share(self, cube)

class ShareValueMap(MappedShares):
    def __init__(self, sharemap: dict):
        self.normalize(sharemap)
        self.sharemap = sharemap

    def share_of(self, axval:str, cube):
        return self.sharemap[axval]

class ShareGetter:
    def share (self, ssys:ShareSystem, cube):
        pass
