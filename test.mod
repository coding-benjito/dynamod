basis: 'c:/develop/dynamod/basis.mod'
parameters:
  $pi = 3.14
properties:
  #
  age:
    values: [age0_15, age16_29, age30_39, age40_44, age45_49, age50_54, age55_59, age60_69, age70_74, age75_79, age80_100]
    shares: [13%,     14%,      9%,       5%,       5%,       6%,       10%,       9%,       8%,       8%,       13%]
  #
  risk:
    values: [high, moderate, low]
    shares:
      for age=age0_15: [5%, 10%, %%]      # '%%' stands for the rest to reach 100%
      for age=age16_29: [6%, 12%, %%]
      #...
      for age=age80_100: [80%, 10%, %%]
      otherwise: [60%, 30%, %%]
  #
  state:
    values: [susceptible, exposed, asymptomatic, presymptomatic, symptomatic, hospitalized, dead, recovered]
    shares:                               # set initial shares
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
  #
  quarantined:
    values: [yes, no]
    shares:
      for state in [exposed, asymptomatic, presymptomatic]:
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
#
# progressions describe time dependent automatic change of properties
# the progression acts on certain compartments and/or with certain probabilities
# and changes the values of properties after a given time distribution 
# The time delay is based on the moment of entering the compartment the progression acts on
#
progression:
  #
  incubation:
    # exposed people getting infectious some (age-dependent) time after exposure
    for state=exposed:
      var days=
        for age=age0_15: 5
        for age=age16_29: 6
          #...
      after.fix(days):                # progression happens after given time
        set state=
          asymptomatic: 18.4%
          presymptomatic: 81.6%
  #
  symptoms_start:
    # presymptomatic people becoming symptomatic after some time
    for state=presymptomatic:
      after.std(2.13, 1.5):           # normal distribution of progression time (mu, sigma)
        set state=symptomatic
  #
  symptoms_worsen:
    # symptomatic people go to hospital, recover or die at home
    for state=symptomatic:
      var prob_hospital = 
        for risk=high: 70%
        for risk=moderate: 25%
        for risk=low: 5%
      var prob_die_at_home = 
        for risk=high: 5%
        for risk=moderate: 1.5%
        for risk=low: 0.1%
      for prob_hospital:
        after.std(5, 3):
          set state=hospitalized
          set quarantined=yes
      for prob_die_at_home:
        after.std(10, 3):
          set state=dead
      otherwise:                     # complement of other probabilities to 100%
        after.std(3.6, 2):
          set state=recovered      
  #
  in_hospital_recover_or_die:
    # hospitalized people either die or recover (within different times)
    for state=hospitalized:
      var prob = 
        for risk=high: 70%
        for risk=moderate: 25%
        for risk=low: 5%
      for prob:
        var duration = 
          for age=age0_16: 10
          #...
          for age=age40_44: 30
          #...
          for age=age80_100: 7
        after.std(duration, duration/2):
          set state=dead
      otherwise:
        var duration = 
          for age=age0_16: 5
          #...
          for age=age40_44: 10
          #...
          for age=age80_100: 3
        after.std(duration, duration/2):
          set state=recovered      
  #
  infection:
    # susceptible people become exposed
    for S as state=susceptible:         # restrict population and give it a name
      for SA as S by age:               # loop over all age categories
        var tprob = 0                    # create and assign numeric variable
        for PA as $$Population with age=SA.age:
          var age_prob = $$User.contact_matrix(SA.age, PA.age)   \
            * (0.231 * PA.share(PA with state=asymptomatic)     \
               + 0.692 * PA.share(PA with state=presymptomatic) \
               + PA.share(PA with state=symptomatic))           \
            * (0.05 * PA.share(PA with quarantined=yes)         \
               + PA.share(PA with quarantined=no))
          tprob = tprob + age_prob
        for tprob:
          set SA.state=exposed
          set SA.quarantined=
            yes: 20%
            no: 80%
  #
  put_in_quarantine:
    #infection is reported, people are put in quarantine
    for quarantined=no:
      for state in [exposed, asymptomatic]:
        for 10%:                        # each day there is a 10% chance of reporting the case
          set quarantined=yes
      for state=symptomatic:
        for 25%:
          set quarantined=yes
results:
  dead_kids = $TotalPersons * $$Population.share($$Population with state=dead with age=age0_16)
  var P7 = $$Population.before(7)
  r = $$Population.share(state=exposed) / P7.share(state=exposed)
