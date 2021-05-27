from dynamod.model import *
from dynamod.optimize import Calibration

import matplotlib.pyplot as plt
import datetime

class Mitigations:
    def __init__(self, start_date):
        self.dtformat = "%d.%m.%Y"
        self.start = datetime.datetime.strptime(start_date, self.dtformat)
        self.sections = []

    def add_section(self, from_date, reduction):
        from_dt = datetime.datetime.strptime(from_date, self.dtformat)
        from_day = (from_dt - self.start).days
        self.sections.append ((from_day, 1-reduction))
        self.sections.sort(key=lambda t: t[0])

    def effect(self, day):
        res = 0
        for from_day, reduction in self.sections:
            if day < from_day:
                break
            res = reduction
        return res

mitigations = Mitigations('01.03.2020')
mitigations.add_section('16.03.2020', 0.813)
mitigations.add_section('01.05.2020', 0.777)
mitigations.add_section('15.05.2020', 0.605)
mitigations.add_section('15.06.2020', 0.614)
mitigations.add_section('07.09.2020', 0.548)
mitigations.add_section('03.11.2020', 0.708)
mitigations.add_section('06.12.2020', 0.685)
mitigations.add_section('08.02.2021', 0.568)

model = parse_model ("austria.mod")
model.initialize(objects={'mitigations':mitigations})
model.run(400)
df = model.history.get_attributes('state')
df.plot()
plt.show()
print (df.to_string())