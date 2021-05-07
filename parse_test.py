from dynamod.dynaprop import *

model = parse_model ("test.mod", trace=False)
model.initialize()
print("totals: ", model.matrix.sum())
model.trace = True
model.step()
print("in: ", model.incoming.sum())
print("out: ", model.outgoing.sum())
print("totals: ", model.matrix.sum())
