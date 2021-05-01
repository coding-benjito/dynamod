from io import StringIO
from antlr4.Utils import escapeWhitespace
from antlr4.tree.Tree import Tree
from antlr4.tree.Trees import Trees

def treeDesc (t: Tree, p, indent=0):
    ruleNames = p.ruleNames
    s = escapeWhitespace(Trees.getNodeText(t, ruleNames), False)
    if t.getChildCount() == 0:
        return s
    with StringIO() as buf:
        buf.write(s + "\n")
        indent += 2
        for i in range(0, t.getChildCount()):
            buf.write(' ' * indent)
            buf.write(treeDesc(t.getChild(i), p, indent) + "\n")
        return buf.getvalue()
