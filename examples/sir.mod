attributes:
    state:
        values: [susceptible, infected, recovered]
        shares: [99.9%, 0.1%, 0]
        
progressions:
    infection:
        for state=susceptible:
            for 0.1 * $(state=infected):
                set state=infected
    recover:
        for state=infected:
            after.fix(20):
                set state=recovered
