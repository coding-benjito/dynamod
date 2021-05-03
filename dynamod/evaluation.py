from dynamod.dynaprop import DynaModel
from dynamod.dynaprop import Partition
from dynamod.core import *

class VarContext:
    def __init__(self, prev=None):
        self.prev = prev
        self.here = []

    def knows (self, key):
        if key in self.here:
            return True
        if self.prev is not None:
            return self.prev.knows (key)
        return False

    def get (self, key):
        if key in self.here:
            return self.here[key]
        if self.prev is not None:
            return self.prev.get (key)
        return None

    def put (self, key, value):
        if value is None:
            self.delete (key)
        if key in self.here or self.prev is None or not self.prev.knows(key):
            self.here[key] = value
        else:
            self.prev.put (key, value)

    def delete (self, key):
        if key in self.here:
            del (self.here[key])
        elif self.prev is not None:
            self.prev.delete (key)

class Evaluator:
    def __init__(self, model: DynaModel, given=None, context=VarContext()):
        self.model = model
        self.given = given
        self.context = context

    def evalComparison (self, opcode, op1, op2):
        if opcode == '<':
            return op1 < op2
        if opcode == '<=':
            return op1 <= op2;
        if opcode == '>':
            return op1 > op2
        if opcode == '>=':
            return op1 >= op2;
        if opcode == '==':
            return op1 == op2
        if opcode == '!=':
            return op1 != op2;
        raise ConfigurationError("unknown comparison operator: " + opcode)

    def evalCalculation(self, opcode, op1, op2):
        if opcode == '+':
            return op1 + op2
        if opcode == '-':
            return op1 - op2;
        if opcode == '*':
            return op1 * op2
        if opcode == '/':
            return op1 / op2;
        raise ConfigurationError("unknown calculation operator: " + opcode)

    def evalCond (self, expr):
        if isinstance(expr, UnaryOp):
            if expr.opcode == 'or':
                for sub in expr.op:
                    if self.evalCond (sub):
                        return True
                return False
            if expr.opcode == 'and':
                for sub in expr.op:
                    if not self.evalCond (sub):
                        return False
                return True
            if expr.opcode == 'not':
                return not self.evalCond (expr.op)
            raise ConfigurationError("unknown condition operation(1): " + expr.opcode, expr.ctx)

        if isinstance(expr, BinaryOp):
            op1 = self.evalExpr(expr.op1)
            op2 = self.evalExpr(expr.op2)
            if is_num(op1) and is_num(op2):
                return self.evalComparison (expr.opcode, op1, op2)
            raise ConfigurationError("illegal comparision", expr.ctx)

        if isinstance(expr, TernaryOp):
            if expr.opcode == 'between':
                val = self.evalExpr(expr.op1)
                limFrom = self.evalExpr(expr.op2)
                limTo = self.evalExpr(expr.op3)
                if is_num(val) and is_num(limFrom) and is_num(limTo):
                    return self.evalComparison('>=', val, limFrom) and self.evalComparison('<=', val, limTo)
                raise ConfigurationError("illegal comparision", expr.ctx)
            raise ConfigurationError("unknown condition operation(3): " + expr.opcode, expr.ctx)

        raise ConfigurationError("unknown condition rule:" + expr)

    def evalExpr (self, expr):
        if isinstance(expr, int) or isinstance(expr, float) or isinstance(expr, str):
            return expr

        if isinstance(expr, UnaryOp):
            if expr.opcode == 'var':
                if self.context.knows (expr.op):
                    return self.context.get (expr.op)
                raise ConfigurationError("unknown variable: " + expr.op, expr.ctx)
            if expr.opcode == 'param':
                if self.model.hasParam (expr.op):
                    return self.model.getParam (expr.op)
                raise ConfigurationError("unknown parameter: " + '$' + expr.op, expr.ctx)
            if expr.opcode == 'syspar':
                val = self.model.getSysParam (expr.op)
                if val is None:
                    raise ConfigurationError("unknown system variable: " + '$$' + expr.op, expr.ctx)
            raise ConfigurationError("unknown expression type(1): " + expr.opcode, expr.ctx)

        if isinstance(expr, BinaryOp):
            if expr.opcode in ['+', '-', '*', '/']:
                op1 = self.evalExpr(expr.op1)
                op2 = self.evalExpr(expr.op2)
                if is_num(op1) and is_num(op2):
                    return self.evalCalculate (expr.opcode, op1, op2)
                raise ConfigurationError("illegal calculation", expr.ctx)
            if expr.opcode == 'func':
                args = []
                if expr.op2 is not None:
                    for op in expr.op2:
                        args.append(self.evalExpr(op))
                return self.model.invokeFunc (expr.op1, args)
            if expr.opcode == 'dot':
                op1 = self.evalExpr(expr.op1)
                if hasattr(op1, expr.op2):
                    return getattr(op1, expr.op2)
                raise ConfigurationError("unknown field " + expr.op2, expr.ctx)
            if expr.opcode == 'by':
                prt = self.evalExpr(expr.op1)
                axis = expr.op2
                if isinstance(prt, Partition):
                    if axis in self.model.properties.prop_map:
                        return prt.partion_by (axis)
                    raise ConfigurationError("unknown property: " + axis, expr.ctx)
                raise ConfigurationError("not a partition", expr.ctx)

            if expr.opcode == 'with':
                prt = self.evalExpr(expr.op1)
                cond = expr.op2
                if isinstance(prt, Partition) and isinstance(cond, DynamodAxisValue):
                    if cond.axis in self.model.properties.prop_map:
                        return prt.partition (cond.axis, cond.value)
                    raise ConfigurationError("unknown property: " + cond.axis, expr.ctx)
                raise ConfigurationError("illegal partition", expr.ctx)
            raise ConfigurationError("unknown expression operation(2): " + expr.opcode, expr.ctx)

        if isinstance(expr, TernaryOp):
            if expr.opcode == 'func':
                args = []
                if expr.op3 is not None:
                    for op in expr.op3:
                        args.append(self.evalExpr(op))
                obj = self.evalExpr(expr.op1)
                method = expr.op2
                if hasattr(obj, method) and callable(obj.method):
                    return obj.method(*args)
                raise ConfigurationError("unknown function call", expr.ctx)
            raise ConfigurationError("unknown expression operation(3): " + expr.opcode, expr.ctx)

        raise ConfigurationError("unknown condition rule:" + expr)


def evalExpr (model: DynaModel, expr, given=None, context=VarContext()):
    return Evaluator(model, given, context).evalExpr(expr)

