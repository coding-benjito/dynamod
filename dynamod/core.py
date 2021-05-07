from recordtype import recordtype
import random
import string

def is_num (expr):
    return isinstance(expr, int) or isinstance(expr, float)

def get_line(ctx):
    if ctx is not None:
        sym = None
        if hasattr(ctx, 'symbol'):
            sym = getattr(ctx, 'symbol')
        elif hasattr(ctx, 'start'):
            sym = getattr(ctx, 'start')
        if hasattr(sym, 'line'):
           return sym.line

def get_random_string(length):
    ''.join(random.choice(string.ascii_letters) for i in range(length))

class MissingAxis(Exception):
    def __init__(self, axis):
        self.axis = axis

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
            if hasattr(sym, 'column'):
                column = sym.column
        if line is not None:
            if column is not None:
                message = '[' + str(line) + ',' + str(column) + '] ' + message
            else:
                message = '[' + str(line) + '] ' + message
        self.message = message

class EvaluationError(ConfigurationError):
    def __init__(self, message, srcfile=None, line=None):
        if srcfile is not None and line is not None:
            message = '[' + srcfile + ':' + line + '] ' + message
        self.message = message


DynamodDesc = recordtype('DynamodDesc', ['basis', 'params', 'properties', 'formulas', 'progressions', 'results'], default=None)
DynamodAttrib = recordtype('DynamodAttrib', ['values', 'shares'])
DynamodAxisValue  = recordtype('DynamodAxisValue', ['ctx', 'axis', 'value'])
DynamodFormula  = recordtype('DynamodFormula', ['ctx', 'name', 'args', 'expr'])
DynamodElseList = recordtype('DynamodElseList', ['ctx', 'list', 'otherwise'])
DynamodVarDef = recordtype('DynamodVarDef', ['ctx', 'varname', 'expression'])
DynamodAfter = recordtype('DynamodAfter', ['ctx', 'distrib', 'args', 'block', 'key'])
DynamodAction = recordtype('DynamodAction', ['ctx', 'axis', 'state'])
DynamodRestriction = recordtype('DynamodRestriction', ['ctx', 'type', 'cond', 'block', ('alias',None)])
DynamodCondExp = recordtype('DynamodCondExp', ['ctx', 'type', 'cond', 'expr'])

TernaryOp = recordtype('TernaryOp', ['ctx', 'opcode', 'op1', 'op2', 'op3'])
BinaryOp = recordtype('BinaryOp', ['ctx', 'opcode', 'op1', 'op2'])
UnaryOp = recordtype('UnaryOp', ['ctx', 'opcode', 'op'])


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
