from antlr4 import *
from dynaparser.DynamodLexer import DynamodLexer
from dynaparser.DynamodParser import DynamodParser
from DynamodBuilder import DynamodBuilder
from dynamod import parse_helper

input = FileStream("test.mod")
lexer = DynamodLexer(input)
stream = CommonTokenStream(lexer)
parser = DynamodParser(stream)
tree = parser.description()
builder = DynamodBuilder(None)
desc = builder.visitDescription(tree)
print(parse_helper.treeDesc(tree, parser))
