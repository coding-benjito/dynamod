from dynamod.dynaprop import *

model = parse_model ("test.mod", trace=False)
model.initialize()
model.step()