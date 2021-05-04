from antlr4 import *
from dynaparser.DynamodLexer import DynamodLexer
from dynaparser.DynamodParser import DynamodParser
from DynamodBuilder import DynamodBuilder
from dynamod import parse_helper
from dynamod.dynaprop import *

input = FileStream("test.mod")
lexer = DynamodLexer(input)
stream = CommonTokenStream(lexer)
parser = DynamodParser(stream)
#parser.setTrace(True)
tree = parser.model()
builder = DynamodBuilder(None)
model = DynaModel(input.name)
builder.visitModel(tree)
model.initialize()