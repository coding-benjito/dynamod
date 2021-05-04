from dynamod.core import *
from dynamod.context import *

class DynamodExpression:
    def __init__(self, model, ctx, name, expr):
        self.srcfile = model.srcfile
        self.line = get_line(ctx)
        self.name = name
        self.expr = expr

    def evaluate(self, context:DynaContext):
        try:
            return Evaluator(context).evalExpr(self.expr)
        except Exception as e:
            raise EvaluationError("failed to evaluate '" + self.name + "'", self.srcfile, self.line) from e

class DynamodFunction:
    def __init__(self, model, ctx, name, args, expr):
        self.srcfile = model.srcfile
        self.line = get_line(ctx)
        self.name = name
        self.args = args
        self.expr = expr

    def evaluate(self, params, context:DynaContext):
        if not isinstance(params, list) or len(params) != len(self.args):
            raise EvaluationError("failed to invoke '" + self.name + "', wrong number of arguments", self.srcfile, self.line)
        localCtx = MapStore()
        for n,v in zip(self.args, params):
            localCtx[n] = v
        try:
            return Evaluator(context.chained_by(localCtx)).evalExpr(self.expr)
        except Exception as e:
            raise EvaluationError("failed to invoke '" + self.name + "'", self.srcfile, self.line) from e

class Evaluator:
    def __init__(self, context:DynaContext):
        self.context = context
        self.model = context.model

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
                from dynamod.dynaprop import Partition
                prt = self.evalExpr(expr.op1)
                axis = expr.op2
                if isinstance(prt, Partition):
                    if axis in self.model.attributes.attr_map:
                        return prt.partion_by (axis)
                    raise ConfigurationError("unknown property: " + axis, expr.ctx)
                raise ConfigurationError("not a partition", expr.ctx)

            if expr.opcode == 'with':
                from dynamod.dynaprop import Partition
                prt = self.evalExpr(expr.op1)
                cond = expr.op2
                if isinstance(prt, Partition) and isinstance(cond, DynamodAxisValue):
                    if cond.axis in self.model.attributes.attr_map:
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
                methodname = expr.op2
                if hasattr(obj, methodname):
                    method = getattr(obj, methodname)
                    if callable(method):
                        return method(*args)
                raise ConfigurationError("unknown function call", expr.ctx)
            raise ConfigurationError("unknown expression operation(3): " + expr.opcode, expr.ctx)

        raise ConfigurationError("unknown condition rule:" + expr)


def evalExpr (expr, context):
    return Evaluator(context).evalExpr(expr)

