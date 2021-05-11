from dynamod.dynaprop import *
import cProfile
import io
import pstats
from pstats import SortKey
import matplotlib.pyplot as plt

def main(runs, profile=False):
    model = parse_model ("test.mod", trace=False)
    #model.trace = True
    #model.trace_for = (2, 0, 4, 1)
    #model.check = True
    model.initialize()
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
    return model


model = main(100, profile=False)
#print (model.history.get_attribute('state', 'exposed'))
pd = model.history.get_attributes('state')
pd.plot()
plt.show()