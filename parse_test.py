from dynamod.dynaprop import *

model = parse_model ("test.mod", trace=False)
model.trace = True
model.trace_for = (2, 0, 4, 1)
model.check = True
model.initialize()
for i in range(100):
    model.step()
print("totals: ", model.matrix.sum())
print(model.history.results)
