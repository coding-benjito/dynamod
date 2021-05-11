#include: 'c:/develop/dynamod/basis.mod'

parameters:
###########
  asymptomatic_share: 18.4%
  f_asymptomatic : 0.231         #factor for infectiousness relative to symptomatic
  f_presymptomatic : 0.692       #factor for infectiousness relative to symptomatic
  factor_when_quarantined : 0.05 #factor for infectiousness relative to unquarantined
  
  contacts_kid_kid : 5           #contact frequency between age groups
  contacts_kid_adult : 2
  contacts_kid_old : 0.5
  contacts_adult_adult : 3
  contacts_adult_old : 1
  contacts_old_old : 2

  infections_per_contact : 0.2
  
attributes:
###########
  age:
    values: (kid, adult, old)
    shares: (17%, 60%,   23%)

  risk:
    values: (high, moderate, low)
    shares:
      for age=kid: (5%, %%, 70%)      # '%%' stands for the rest to reach 100%
      for age=old: (60%, %%, 8%)
      otherwise: (18%, %%, 20%)

  state:
    values: (susceptible, exposed, asymptomatic, presymptomatic, symptomatic, hospitalized, dead, recovered)
    shares:                               
      susceptible: 90%
      recovered: 6%
      presymptomatic: 0.4%
      exposed: 0.6%
      asymptomatic:
        for risk=low: 1.5%
        for risk=moderate: 0.75%
        for risk=high: 0.15%
      symptomatic:
        for risk=low: 1.2%
        for risk=moderate: 1.95%
        for risk=high: 2.1%
      hospitalized:
        for risk=low: 0.3%
        for risk=moderate: 0.3%
        for risk=high: 0.75%
      dead: 0

  quarantined:
    values: (yes, no)
    shares:
      for state in (exposed, asymptomatic, presymptomatic):
        yes: 10%
        no: 90%
      for state=symptomatic:
        yes: 60%
        no: 40%
      for state=hospitalized:
        yes: 98%
        no: 2%
      otherwise:
        yes: 0
        no: %%


formulas:
#########
  Kids: ALL with age=kid
  Adults: ALL with age=adult
  Olds: ALL with age=old
  infected(X): [state=symptomatic|X] + f_asymptomatic*[state=asymptomatic|X] + f_presymptomatic*[state=presymptomatic|X]
  force(X): infected(X with quarantined=no) + factor_when_quarantined * infected(X with quarantined=yes)
  force_of_infection: 
    for age=kid: contacts_kid_kid * force(Kids) + contacts_kid_adult * force(Adults) + contacts_kid_old * force(Olds)
    for age=adult: contacts_kid_adult * force(Kids) + contacts_adult_adult * force(Adults) + contacts_adult_old * force(Olds)
    for age=old: contacts_kid_old * force(Kids) + contacts_adult_old * force(Adults) + contacts_old_old * force(Olds)
  infection_probability: infections_per_contact * force_of_infection
  Yesterday: ALL.before(1)


#
# progressions describe the change of attributes over time
# the progression acts on certain compartments and/or with certain probabilities
# and/or changes the values of properties after a given time distribution 
# The time delay is based on the moment of entering the compartment the progression acts on
#
progressions:
#############
  incubation:
    # exposed people getting infectious some (age-dependent) time after exposure
    for state=exposed:
      var days=
        for age=kid: 5
        for age=old: 4
        for age=adult: 6
      after.fix(days):                # progression happens after given time
        set state=
          asymptomatic: asymptomatic_share
          presymptomatic: 1 - asymptomatic_share

  symptoms_start:
    # presymptomatic people becoming symptomatic after some time
    for state=presymptomatic:
      after.std(2.13, 1.5):           # normal distribution of progression time (mu, sigma)
        set state=symptomatic

  symptoms_worsen:
    # symptomatic people go to hospital, recover or die at home
    for state=symptomatic:
      var prob_hospital = 
        for risk=high: 70%
        for risk=moderate: 25%
        for risk=low: 5%
      for prob_hospital:
        after.std(5, 3):
          set state=hospitalized
          set quarantined=yes
      otherwise:
        var prob_die_at_home = 
          for risk=high: 5%
          for risk=moderate: 1.5%
          for risk=low: 0.1%
        for prob_die_at_home:
          after.std(10, 3):
            set state=dead
        otherwise:                     # complement of other probabilities to 100%
          after.std(3.6, 2):
            set state=recovered      

  in_hospital_recover_or_die:
    # hospitalized people either die or recover (within different times)
    for state=hospitalized:
      var prob = 
        for risk=high: 70%
        for risk=moderate: 25%
        for risk=low: 5%
      for prob:
        var duration = 
          for age=kid: 10
          for age=adult: 30
          for age=old: 7
        after.std(duration, duration/2):
          set state=dead
      otherwise:
        var duration = 
          for age=kid: 5
          for age=adult: 10
          for age=old: 3
        after.std(duration, duration/2):
          set state=recovered      

  infection:
    # susceptible people become exposed
    for S as state=susceptible:         
      for infection_probability:
        set state=exposed
        set quarantined=
          yes: 20%
          no: 80%

  put_in_quarantine:
    #infection is reported, people are put in quarantine
    for quarantined=no:
      for state in (exposed, asymptomatic, presymptomatic):
        for 10%:                        # each day there is a 10% chance of reporting the case
          set quarantined=yes
      for state=symptomatic:
        for 25%:
          set quarantined=yes
          
results:
########
  dead_kids = [state=dead with age=kid]
  exposed = [state=exposed]
  r = 5.2 * [state=exposed] / [Yesterday with state=exposed]

