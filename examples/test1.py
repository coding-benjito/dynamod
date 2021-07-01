from dynamod.model import *

import matplotlib.pyplot as plt
import datetime

model = parse_model ("example1.mod")
model.initialize()
model.run(400)
df = model.history.get_attributes('state')
df.plot()
plt.show()
