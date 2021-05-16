extends: 'c:/develop/dynamod/example.mod'

parameters:
###########
    lockdown_limit: 200 
    delay: 5   

formulas:
#########
    # the calculation of the infection probability is redefined to include our measures
    infection_probability: infections_per_contact * force_of_infection * measures

    # the 7-day incidence some days back is calculated
    incidence(b): 100000 * NewInfections(ALL.before(b),7)

    # reduction by lockdown measures
    measures: 
        if day in [50..100]: 0.3
        if day >= 100 and incidence(delay) > lockdown_limit: 0.6
        otherwise: 1

    
