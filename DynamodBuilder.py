from dynaparser.DynamodVisitor import DynamodVisitor
from dynaparser.DynamodParser import DynamodParser
from antlr4 import ParserRuleContext
from dynamod.core import *

def to_dict (item):
    if item is None:
        return None
    if isinstance(item, tuple):
        return {item[0]: item[1]}
    if isinstance(item, list):
        map = {}
        for entry in item:
            map[entry[0]] = entry[1]
        return map
    if isinstance(item, dict):
        return item
    raise ValueError("to_dict() called on " + type(item))

def to_number (txt):
    try:
        return int(txt)
    except ValueError:
        return float(txt)

class DynamodBuilder(DynamodVisitor):
    def __init__(self, context):
        self.context = context

    def visit (self, ctx:ParserRuleContext):
        return ctx.accept(self) if ctx is not None else None

    def visitDescription(self, ctx:DynamodParser.DescriptionContext):
        return DynamodDesc(ctx.PATH().getText(),
                           to_dict(self.visit(ctx.parameters_block().parameters())),
                           to_dict(self.visit(ctx.properties_block().properties())),
                           to_dict(self.visit(ctx.progressions_block().progressions())))

    # Visit a parse tree produced by DynamodParser#params_item.
    def visitParams_item(self, ctx:DynamodParser.Params_itemContext):
        return self.visit(ctx.parameter())

    # Visit a parse tree produced by DynamodParser#params_rep.
    def visitParams_rep(self, ctx:DynamodParser.Params_repContext):
        map = self.visit(ctx.parameters())
        map.update (to_dict(self.visit(ctx.parameter())))
        return map

    # Visit a parse tree produced by DynamodParser#parameter.
    def visitParameter(self, ctx:DynamodParser.ParameterContext):
        return (ctx.NAME().getText(), self.visit(ctx.expression()))

    # Visit a parse tree produced by DynamodParser#properties_item.
    def visitProperties_item(self, ctx:DynamodParser.Properties_itemContext):
        return to_dict((ctx.NAME().getText(), self.visit(ctx.property_block())))

    # Visit a parse tree produced by DynamodParser#properties_rep.
    def visitProperties_rep(self, ctx:DynamodParser.Properties_repContext):
        map = self.visit(ctx.properties())
        map[ctx.NAME().getText()] = self.visit(ctx.property_block())
        return map

    # Visit a parse tree produced by DynamodParser#property_block.
    def visitProperty_block(self, ctx:DynamodParser.Property_blockContext):
        prop = DynamodProp(self.visit(ctx.values()), self.visit(ctx.shares()))
        if isinstance(prop.shares, list):
            if len(prop.shares) != len(prop.values):
                raise ConfigurationError("share list has wrong number of entries", ctx.shares())
            map = {}
            for v,s in zip(prop.values, prop.shares):
                map[v] = s
            prop.shares = map
        return prop

    # Visit a parse tree produced by DynamodParser#shares_as_list.
    def visitShares_as_list(self, ctx:DynamodParser.Shares_as_listContext):
        return self.visit(ctx.expression_list())

    # Visit a parse tree produced by DynamodParser#shares_as_map.
    def visitShares_as_map(self, ctx:DynamodParser.Shares_as_mapContext):
        return self.visit(ctx.share_map_block())

    # Visit a parse tree produced by DynamodParser#shares_as_cond.
    def visitShares_as_cond(self, ctx:DynamodParser.Shares_as_condContext):
        return self.visit(ctx.cond_shares_block())

    # Visit a parse tree produced by DynamodParser#share_map_block.
    def visitShare_map_block(self, ctx:DynamodParser.Share_map_blockContext):
        return self.visit(ctx.share_map())

    # Visit a parse tree produced by DynamodParser#share_map_rep.
    def visitShare_map_rep(self, ctx:DynamodParser.Share_map_repContext):
        map = self.visit(ctx.share_map())
        map[ctx.NAME().getText()] = self.visit(ctx.pexpression())
        return map


    # Visit a parse tree produced by DynamodParser#share_map_item.
    def visitShare_map_item(self, ctx:DynamodParser.Share_map_itemContext):
        return to_dict((ctx.NAME().getText(), self.visit(ctx.pexpression())))

    # Visit a parse tree produced by DynamodParser#cond_shares_block.
    def visitCond_shares_block(self, ctx:DynamodParser.Cond_shares_blockContext):
        return DynamodElseList(self.visit(ctx.cond_shares()), self.visit(ctx.shares()))

    # Visit a parse tree produced by DynamodParser#cond_shares_item.
    def visitCond_shares_item(self, ctx:DynamodParser.Cond_shares_itemContext):
        return [(self.visit(ctx.condition()), self.visit(ctx.shares()))]

    # Visit a parse tree produced by DynamodParser#cond_shares_rep.
    def visitCond_shares_rep(self, ctx:DynamodParser.Cond_shares_repContext):
        list = self.visit(ctx.cond_shares())
        list.append ((self.visit(ctx.condition()), self.visit(ctx.shares())))
        return list

    # Visit a parse tree produced by DynamodParser#pexpr_as_simple.
    def visitPexpr_as_simple(self, ctx:DynamodParser.Pexpr_as_simpleContext):
        return self.visit(ctx.expression())

    # Visit a parse tree produced by DynamodParser#pexpr_as_block.
    def visitPexpr_as_block(self, ctx:DynamodParser.Pexpr_as_blockContext):
        return self.visit(ctx.pexpression_block())


    # Visit a parse tree produced by DynamodParser#pexpression_block.
    def visitPexpression_block(self, ctx:DynamodParser.Pexpression_blockContext):
        return DynamodElseList(self.visit(ctx.pexpressions()), self.visit(ctx.pexpression()))

    # Visit a parse tree produced by DynamodParser#pexpressions_item.
    def visitPexpressions_item(self, ctx:DynamodParser.Pexpressions_itemContext):
        return [(self.visit(ctx.condition()), self.visit(ctx.pexpression()))]

    # Visit a parse tree produced by DynamodParser#pexpressions_rep.
    def visitPexpressions_rep(self, ctx:DynamodParser.Pexpressions_repContext):
        list = self.visit(ctx.pexpressions())
        list.append ((self.visit(ctx.condition()), self.visit(ctx.pexpression())))
        return list

    # Visit a parse tree produced by DynamodParser#cond_as_eq.
    def visitCond_as_eq(self, ctx:DynamodParser.Cond_as_eqContext):
        return (ctx.NAME().getText(), self.visit(ctx.expression()))

    # Visit a parse tree produced by DynamodParser#cond_as_in.
    def visitCond_as_in(self, ctx:DynamodParser.Cond_as_inContext):
        return (ctx.NAME().getText(), self.visit(ctx.values()))

    # Visit a parse tree produced by DynamodParser#cond_as_expr.
    def visitCond_as_expr(self, ctx:DynamodParser.Cond_as_exprContext):
        return self.visit(ctx.expression())

    # Visit a parse tree produced by DynamodParser#values.
    def visitValues(self, ctx:DynamodParser.ValuesContext):
        list = []
        for entry in ctx.vals:
            list.append(entry.text)
        return list

    # Visit a parse tree produced by DynamodParser#expression_list.
    def visitExpression_list(self, ctx:DynamodParser.Expression_listContext):
        list = []
        for entry in ctx.exprs:
            list.append(self.visit(entry))
        return list

    # Visit a parse tree produced by DynamodParser#progressions_item.
    def visitProgressions_item(self, ctx:DynamodParser.Progressions_itemContext):
        return to_dict((ctx.NAME().getText(), self.visit(ctx.progression_block())))

    # Visit a parse tree produced by DynamodParser#progressions_rep.
    def visitProgressions_rep(self, ctx:DynamodParser.Progressions_repContext):
        map = self.visit(ctx.progressions())
        map[ctx.NAME().getText()] = self.visit(ctx.progression_block())
        return map

    # Visit a parse tree produced by DynamodParser#progression_block.
    def visitProgression_block(self, ctx:DynamodParser.Progression_blockContext):
        return self.visit(ctx.progression())

    # Visit a parse tree produced by DynamodParser#progression_rep.
    def visitProgression_rep(self, ctx:DynamodParser.Progression_repContext):
        list = self.visit(ctx.progression())
        list.extend(self.visit(ctx.progression_component()))
        return list

    # Visit a parse tree produced by DynamodParser#progression_item.
    def visitProgression_item(self, ctx:DynamodParser.Progression_itemContext):
        return [self.visit(ctx.progression_component())]

    # Visit a parse tree produced by DynamodParser#prog_vardef.
    def visitProg_vardef(self, ctx:DynamodParser.Prog_vardefContext):
        return self.visit(ctx.variable_definition())

    # Visit a parse tree produced by DynamodParser#prog_restrictions.
    def visitProg_restrictions(self, ctx:DynamodParser.Prog_restrictionsContext):
        list = []
        for r in ctx.restr:
            list.append(self.visit(r))
        return DynamodElseList(list, self.visit(ctx.progression_block()))

    # Visit a parse tree produced by DynamodParser#prog_after.
    def visitProg_after(self, ctx:DynamodParser.Prog_afterContext):
        return self.visit(ctx.progression_after())

    # Visit a parse tree produced by DynamodParser#prog_action.
    def visitProg_action(self, ctx:DynamodParser.Prog_actionContext):
        return self.visit(ctx.progression_action())

    # Visit a parse tree produced by DynamodParser#restriction.
    def visitRestriction(self, ctx:DynamodParser.RestrictionContext):
        res = DynamodRestriction(self.visit(ctx.condition()), self.visit(ctx.progression_block()))
        if ctx.NAME() is not None:
            res.alias = ctx.NAME().getText()
        return res

    # Visit a parse tree produced by DynamodParser#progression_after.
    def visitProgression_after(self, ctx:DynamodParser.Progression_afterContext):
        return DynamodAfter(ctx.NAME().getText(), self.visit(ctx.arguments()), self.visit(ctx.progression_block()))

    # Visit a parse tree produced by DynamodParser#progression_action.
    def visitProgression_action(self, ctx:DynamodParser.Progression_actionContext):
        return DynamodAction(self.visit(ctx.axis), self.visit(ctx.pstate()))

    # Visit a parse tree produced by DynamodParser#pstate_name.
    def visitPstate_name(self, ctx:DynamodParser.Pstate_nameContext):
        return ctx.NAME().getText()

    # Visit a parse tree produced by DynamodParser#pstate_block.
    def visitPstate_block(self, ctx:DynamodParser.Pstate_blockContext):
        return self.visit(ctx.share_map_block())

    # Visit a parse tree produced by DynamodParser#variable_definition.
    def visitVariable_definition(self, ctx:DynamodParser.Variable_definitionContext):
        return DynamodVarDef(ctx.NAME().getText(), self.visit(ctx.pexpression()))


    # Visit a parse tree produced by DynamodParser#exp_by.
    def visitExp_by(self, ctx:DynamodParser.Exp_byContext):
        return BinaryOp('by', self.visit(ctx.expression()), ctx.NAME().getText())

    # Visit a parse tree produced by DynamodParser#exp_with.
    def visitExp_with(self, ctx:DynamodParser.Exp_withContext):
        return BinaryOp('with', self.visit(ctx.expression()), self.visit(ctx.condition()))

    # Visit a parse tree produced by DynamodParser#exp_term.
    def visitExp_term(self, ctx:DynamodParser.Exp_termContext):
        return self.visit(ctx.term())

    # Visit a parse tree produced by DynamodParser#exp_sub.
    def visitExp_sub(self, ctx:DynamodParser.Exp_subContext):
        return BinaryOp('-', self.visit(ctx.expression()), self.visit(ctx.term()))

    # Visit a parse tree produced by DynamodParser#exp_add.
    def visitExp_add(self, ctx:DynamodParser.Exp_addContext):
        return BinaryOp('-', self.visit(ctx.expression()), self.visit(ctx.term()))

    # Visit a parse tree produced by DynamodParser#term_mul.
    def visitTerm_mul(self, ctx:DynamodParser.Term_mulContext):
        return BinaryOp('*', self.visit(ctx.term()), self.visit(ctx.factor()))

    # Visit a parse tree produced by DynamodParser#term_factor.
    def visitTerm_factor(self, ctx:DynamodParser.Term_factorContext):
        return self.visit(ctx.factor())

    # Visit a parse tree produced by DynamodParser#term_div.
    def visitTerm_div(self, ctx:DynamodParser.Term_divContext):
        return BinaryOp('/', self.visit(ctx.term()), self.visit(ctx.factor()))

    # Visit a parse tree produced by DynamodParser#factor_pos.
    def visitFactor_pos(self, ctx:DynamodParser.Factor_posContext):
        return self.visit(ctx.factor())

    # Visit a parse tree produced by DynamodParser#factor_neg.
    def visitFactor_neg(self, ctx:DynamodParser.Factor_negContext):
        return UnaryOp('-', self.visit(ctx.factor()))

    # Visit a parse tree produced by DynamodParser#factor_primary.
    def visitFactor_primary(self, ctx:DynamodParser.Factor_primaryContext):
        return self.visit(ctx.primary())

    # Visit a parse tree produced by DynamodParser#factor_expr.
    def visitFactor_expr(self, ctx:DynamodParser.Factor_exprContext):
        return self.visit(ctx.expression())

    # Visit a parse tree produced by DynamodParser#factor_number.
    def visitFactor_number(self, ctx:DynamodParser.Factor_numberContext):
        try:
            return to_number(ctx.NUMBER().getText())
        except ValueError:
            raise ConfigurationError("illegal number format: " + ctx.NUMBER().getText(), ctx.NUMBER())

    # Visit a parse tree produced by DynamodParser#factor_percent.
    def visitFactor_percent(self, ctx:DynamodParser.Factor_percentContext):
        try:
            return to_number(ctx.NUMBER().getText()) / 100
        except ValueError:
            raise ConfigurationError("illegal number format: " + ctx.NUMBER().getText(), ctx.NUMBER())

    # Visit a parse tree produced by DynamodParser#factor_rest.
    def visitFactor_rest(self, ctx:DynamodParser.Factor_restContext):
        return -1

    # Visit a parse tree produced by DynamodParser#primary_func.
    def visitPrimary_func(self, ctx:DynamodParser.Primary_funcContext):
        return BinaryOp('func', self.visit(ctx.primary()), self.visit(ctx.arguments()))

    # Visit a parse tree produced by DynamodParser#primary_dot.
    def visitPrimary_dot(self, ctx:DynamodParser.Primary_dotContext):
        return BinaryOp('dot', self.visit(ctx.primary()), ctx.NAME().getText())

    # Visit a parse tree produced by DynamodParser#primary_system.
    def visitPrimary_system(self, ctx:DynamodParser.Primary_systemContext):
        return UnaryOp('syspar', ctx.NAME().getText())

    # Visit a parse tree produced by DynamodParser#primary_name.
    def visitPrimary_name(self, ctx:DynamodParser.Primary_nameContext):
        return ctx.NAME().getText()

    # Visit a parse tree produced by DynamodParser#primary_param.
    def visitPrimary_param(self, ctx:DynamodParser.Primary_paramContext):
        return UnaryOp('param', ctx.NAME().getText())

    # Visit a parse tree produced by DynamodParser#arguments.
    def visitArguments(self, ctx:DynamodParser.ArgumentsContext):
        list = []
        for a in ctx.args:
            list.append(self.visit(a))

