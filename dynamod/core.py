from recordtype import recordtype
from collections import OrderedDict
import random
import string

NOSLICE = slice(None)

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
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def deslice(org):
    return tuple([None if x is NOSLICE else x for x in org])

def reslice(org):
    return tuple([NOSLICE if x is None else x for x in org])

def short_str (seg):
    return '[' + ','.join(':' if s is None or s is NOSLICE else str(s) for s in seg) + ']'

def leads_into(seg, sout, sin):
    outside = False
    for (ihere, ifrom, ito) in zip(seg, sout, sin):
        #rules: no lists in ifrom and ito
        #       if one of ifrom/ito is NOSLICE, then the other one is NOSLICE too
        if ihere is not NOSLICE and ifrom is not NOSLICE:
            if ifrom == ito:
                if ihere != ifrom:
                    return False    #doesn't lead in
            else:
                if isinstance(ihere, list):
                    if ito not in ihere:
                        return False    #doesn't lead in
                    if ifrom not in ihere:
                        outside = True       #may lead out
                else:
                    if ito != ihere:
                        return False    #doesn't lead in
                    if ifrom != ihere:
                        outside = True      #may lead out
    return outside

def intersect(seg1, seg2):
    res = []
    sub1 = []
    sub2 = []
    for s1,s2 in zip(seg1, seg2):
        if s1 is NOSLICE:
            if s2 is NOSLICE:
                res.append(NOSLICE)
                sub1.append(NOSLICE)
                sub2.append(NOSLICE)
            else:
                res.append(s2)
                sub1.append(s2)
        else:
            if s2 is NOSLICE:
                res.append(s1)
                sub2.append(s1)
            elif s1 == s2:
                res.append(s1)
            else:
                return (None, None, None)
    return (tuple(res), tuple(sub1), tuple(sub2))

def axis_exclude (model, axis):
    return tuple([att.index for att in model.attSystem.attributes if att.name != axis])

def axval_segment (model, axis, value):
    return tuple([att.values.index(value) if att.name == axis else NOSLICE for att in model.attSystem.attributes])

def modified_seg(seg, index, value):
    return tuple([value if i==index else seg[i] for i in range(len(seg))])

def insert_at (map:dict, key, value, at):
    res = OrderedDict()
    found = False
    for k, v in map.items():
        if k == at:
            res[key] = value
            found = True
        res[k] = v
    if not found:
        res[key] = value
    return res

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

