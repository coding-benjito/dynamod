from dynamod.model import *
import cProfile
import io
import pstats
from pstats import SortKey
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from  dynamod.parse_helper import *

profile = True
runs = 150
np.seterr(all='raise')

model = parse_model ("t5.mod", trace=False)
#model.trace_for = (2, 0, 4, 1)
#model.check = True
model.initialize()
#model.trace_on({'state':'exposed'})
#model.trace = True
#model.check = True
#model.raw_errors = True

if profile:
    pr = cProfile.Profile()
    pr.enable()
for i in range(runs):
    model.step()
if profile:
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.TIME
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

print ("")
print (model.history.get_result('onceinfected'))
print (model.history.get_result('dailynew'))
print (model.history.get_result('r4'))
print (model.history.get_result('incidence7'))
pd1 = model.history.get_attributes('state')
pd2 = model.history.get_attributes('quarantined')
#pd.concat([pd1, pd2]).plot()
pd1.plot()
plt.show()