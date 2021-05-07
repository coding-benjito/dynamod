from dynamod.core import MissingAxis, ConfigurationError, get_line

class Action:
    error_stack = None
    ctx_stack = []

    def __init__(self, desc=None, op=None, ctx=None, line=None):
        self.desc = desc
        if op is not None and hasattr(op, "ctx"):
            ctx = op.ctx
        if ctx is not None:
            line = get_line (ctx)
        self.line = line

    def __enter__(self):
        Action.ctx_stack.append (self)

    def __exit__(self, exc_type, exc_value, traceback):
        if Action.error_stack is None and exc_type is not None and exc_type != MissingAxis:
            Action.error_stack = Action.ctx_stack.copy()
        Action.ctx_stack.pop()

    def to_text(self):
        return (self.desc if self.desc is not None else "error") + ((" in line " + str(self.line)) if self.line is not None and self.line is not False else "")

def report_actions (e):
    lines = set()
    print ("an error occurred:" + (e.message if hasattr(e, 'message') else str(e.args)))
    print ("logical operation stack:")
    if Action.error_stack is not None:
        for action in Action.error_stack[::-1]:
            if action.line == None:
                continue
            if action.line == False or action.line not in lines:
                print ("  ***", action.to_text())
                lines.add(action.line)
        Action.error_stack = None
    if not isinstance(e, ConfigurationError):
        raise e from None
