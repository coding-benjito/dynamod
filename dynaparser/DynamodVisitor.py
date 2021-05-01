# Generated from Dynamod.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DynamodParser import DynamodParser
else:
    from DynamodParser import DynamodParser

# This class defines a complete generic visitor for a parse tree produced by DynamodParser.

class DynamodVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DynamodParser#description.
    def visitDescription(self, ctx:DynamodParser.DescriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#parameters_block.
    def visitParameters_block(self, ctx:DynamodParser.Parameters_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#params_item.
    def visitParams_item(self, ctx:DynamodParser.Params_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#params_rep.
    def visitParams_rep(self, ctx:DynamodParser.Params_repContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#parameter.
    def visitParameter(self, ctx:DynamodParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#properties_block.
    def visitProperties_block(self, ctx:DynamodParser.Properties_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#properties_item.
    def visitProperties_item(self, ctx:DynamodParser.Properties_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#properties_rep.
    def visitProperties_rep(self, ctx:DynamodParser.Properties_repContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#property_block.
    def visitProperty_block(self, ctx:DynamodParser.Property_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#shares_as_list.
    def visitShares_as_list(self, ctx:DynamodParser.Shares_as_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#shares_as_map.
    def visitShares_as_map(self, ctx:DynamodParser.Shares_as_mapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#shares_as_cond.
    def visitShares_as_cond(self, ctx:DynamodParser.Shares_as_condContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#share_map_block.
    def visitShare_map_block(self, ctx:DynamodParser.Share_map_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#share_map_rep.
    def visitShare_map_rep(self, ctx:DynamodParser.Share_map_repContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#share_map_item.
    def visitShare_map_item(self, ctx:DynamodParser.Share_map_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#cond_shares_block.
    def visitCond_shares_block(self, ctx:DynamodParser.Cond_shares_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#cond_shares_item.
    def visitCond_shares_item(self, ctx:DynamodParser.Cond_shares_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#cond_shares_rep.
    def visitCond_shares_rep(self, ctx:DynamodParser.Cond_shares_repContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#pexpr_as_simple.
    def visitPexpr_as_simple(self, ctx:DynamodParser.Pexpr_as_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#pexpr_as_block.
    def visitPexpr_as_block(self, ctx:DynamodParser.Pexpr_as_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#pexpression_block.
    def visitPexpression_block(self, ctx:DynamodParser.Pexpression_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#pexpressions_item.
    def visitPexpressions_item(self, ctx:DynamodParser.Pexpressions_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#pexpressions_rep.
    def visitPexpressions_rep(self, ctx:DynamodParser.Pexpressions_repContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#cond_as_eq.
    def visitCond_as_eq(self, ctx:DynamodParser.Cond_as_eqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#cond_as_in.
    def visitCond_as_in(self, ctx:DynamodParser.Cond_as_inContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#cond_as_expr.
    def visitCond_as_expr(self, ctx:DynamodParser.Cond_as_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#values.
    def visitValues(self, ctx:DynamodParser.ValuesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#expression_list.
    def visitExpression_list(self, ctx:DynamodParser.Expression_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#progressions_block.
    def visitProgressions_block(self, ctx:DynamodParser.Progressions_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#progressions_item.
    def visitProgressions_item(self, ctx:DynamodParser.Progressions_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#progressions_rep.
    def visitProgressions_rep(self, ctx:DynamodParser.Progressions_repContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#progression_block.
    def visitProgression_block(self, ctx:DynamodParser.Progression_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#progression_rep.
    def visitProgression_rep(self, ctx:DynamodParser.Progression_repContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#progression_item.
    def visitProgression_item(self, ctx:DynamodParser.Progression_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#prog_vardef.
    def visitProg_vardef(self, ctx:DynamodParser.Prog_vardefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#prog_restrictions.
    def visitProg_restrictions(self, ctx:DynamodParser.Prog_restrictionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#prog_after.
    def visitProg_after(self, ctx:DynamodParser.Prog_afterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#prog_action.
    def visitProg_action(self, ctx:DynamodParser.Prog_actionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#restriction.
    def visitRestriction(self, ctx:DynamodParser.RestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#progression_after.
    def visitProgression_after(self, ctx:DynamodParser.Progression_afterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#progression_action.
    def visitProgression_action(self, ctx:DynamodParser.Progression_actionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#pstate_name.
    def visitPstate_name(self, ctx:DynamodParser.Pstate_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#pstate_block.
    def visitPstate_block(self, ctx:DynamodParser.Pstate_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#variable_definition.
    def visitVariable_definition(self, ctx:DynamodParser.Variable_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#exp_by.
    def visitExp_by(self, ctx:DynamodParser.Exp_byContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#exp_with.
    def visitExp_with(self, ctx:DynamodParser.Exp_withContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#exp_term.
    def visitExp_term(self, ctx:DynamodParser.Exp_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#exp_sub.
    def visitExp_sub(self, ctx:DynamodParser.Exp_subContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#exp_add.
    def visitExp_add(self, ctx:DynamodParser.Exp_addContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#term_mul.
    def visitTerm_mul(self, ctx:DynamodParser.Term_mulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#term_factor.
    def visitTerm_factor(self, ctx:DynamodParser.Term_factorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#term_div.
    def visitTerm_div(self, ctx:DynamodParser.Term_divContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#factor_pos.
    def visitFactor_pos(self, ctx:DynamodParser.Factor_posContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#factor_neg.
    def visitFactor_neg(self, ctx:DynamodParser.Factor_negContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#factor_primary.
    def visitFactor_primary(self, ctx:DynamodParser.Factor_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#factor_expr.
    def visitFactor_expr(self, ctx:DynamodParser.Factor_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#factor_number.
    def visitFactor_number(self, ctx:DynamodParser.Factor_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#factor_percent.
    def visitFactor_percent(self, ctx:DynamodParser.Factor_percentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#factor_rest.
    def visitFactor_rest(self, ctx:DynamodParser.Factor_restContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#primary_func.
    def visitPrimary_func(self, ctx:DynamodParser.Primary_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#primary_dot.
    def visitPrimary_dot(self, ctx:DynamodParser.Primary_dotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#primary_system.
    def visitPrimary_system(self, ctx:DynamodParser.Primary_systemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#primary_name.
    def visitPrimary_name(self, ctx:DynamodParser.Primary_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#primary_param.
    def visitPrimary_param(self, ctx:DynamodParser.Primary_paramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DynamodParser#arguments.
    def visitArguments(self, ctx:DynamodParser.ArgumentsContext):
        return self.visitChildren(ctx)



del DynamodParser