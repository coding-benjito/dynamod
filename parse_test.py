from dynamod.dynaprop import *
import cProfile
import io
import pstats
from pstats import SortKey
import matplotlib.pyplot as plt

profile = False
runs = 100
model = parse_model ("test.mod", trace=False)
#model.trace = True
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

pd = model.history.get_attributes('state')
pd.plot()
plt.show()