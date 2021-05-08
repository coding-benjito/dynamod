import numpy as np
from dynamod.core import *

def check_nonnegatives(model):
    matrix = model.matrix + model.incoming + model.outgoing
    if np.amin(matrix) < -0.00000001:
        at = np.unravel_index(np.argmin(matrix), matrix.shape)
        print ("!!! negative share for ", end='')
        for att, index in zip(model.attSystem.attributes, at):
            print (att.name + ":" + att.values[index], end=', ')
        print(" entrycode", at)
        raise EvaluationError("negative matrix entries")

def check_changes(model):
    matrix = model.matrix + model.incoming + model.outgoing
    value = matrix[model.trace_for]
    if value != model.trace_val:
        print("value changed from", model.trace_val, "to", value)
        model.trace_val = value

