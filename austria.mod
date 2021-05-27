attributes:
###########
    age:
        values: [to10, to20, to30, t040, to50, to60, to70, to80, plus80]
        shares: [0.096561771, 0.097335918, 0.128061837, 0.135811554, 0.136499234, 0.15605634, 0.111673002, 0.088047952, 0.049952392]

    state:
        values: [susceptible, exposed, infectious, quarantined, hospitalized, icu, deceased, recovered]
        shares: [%%,          1E-5,    0,          0,           0,            0,   0,        0] 
        
    severity:
        values: [unnoticed, mild, hospital, critical]
        shares: [1,         0,    0,        0]


progressions:
#############
    infection:
        # susceptible people become exposed
        for state=susceptible:                 
            for infection_probability:
                set state=exposed

    latency:
        # exposed people getting infectious, their severity is decided
        for S as state=exposed:
            after.std(latency_period, 1):
                set state=infectious
                for detection_ratio:
                    for hospitalization_rate[S.age]:
                        for critical_ratio[S.age]:
                            set severity=critical
                        otherwise:
                            set severity=hospital
                    otherwise:
                        set severity=mild
                otherwise:
                    set severity=unnoticed        

    incubation:
        # infectious people develop symptoms and are quarantined, or recover without symptoms
        for state=infectious:
            after.std(infectious_period, 1):
                for severity=unnoticed:
                    set state=recovered
                otherwise:
                    set state=quarantined

    hospitalization:
        # quarantined people got to hospital, icu or recover directly
        for state=quarantined:
            for severity=mild:
                after.fix(quarantine_time_before_recovery):
                    set state=recovered
            for severity=hospital:
                after.fix(quarantine_time_before_hospital):
                    set state=hospitalized
            for severity=critical:
                after.fix(quarantine_time_before_icu):
                    set state=icu

    recover_in_hospital:
        for state=hospitalized:
            after.fix(time_in_hospital):
                set state=recovered
                
    progress_in_icu:
        for S as state=icu:
            after.fix(time_in_icu):
                for death_rate(S):
                    set state=deceased
                otherwise:
                    set state=hospitalized
                

parameters:
###########
    R0: 3.1977
    seasonal_weight: 0.1
    seasonal_peak: 320    # day 320 is Jan 15th, 2021
    latency_period: 3
    infectious_period: 3
    quarantine_time_before_recovery: 10
    quarantine_time_before_hospital: 10
    quarantine_time_before_icu: 10
    time_in_hospital: 11.5
    time_in_icu: 6.5
    total_population: 8858775
    icu_overload_severity_factor: 2
    
    # age-specific parameters
    hospitalization_rate: [0.1%, 0.2%, 1%, 1.8%, 2.5%, 4%, 7.3%, 12%, 50%]
    critical_ratio: [20%, 15%, 12%, 15%, 20%, 22%, 32%, 45%, 50%]
    death_in_icu: [3%, 5%, 8%, 8%, 12%, 15%, 30%, 45%, 50%]

formulas:
#########
    infection_probability: $(state=infectious) * R0/infectious_period * mitigation_factor * seasonal_factor
    mitigation_factor: 1 - mitigations.effect(day)
    seasonal_factor: 1 - seasonal_weight/2 * (1 - cos((day - seasonal_peak) * 2 * PI / 365))
    detection_ratio:          #day 0 is March 1st, 2020
        if day <= 30: 15%     #day 30 is March 31st, 2020
        if day <= 78: 15% + 36% * (day - 30) / (78 - 30)
        otherwise: 47%
    death_rate(S): min(1, death_in_icu[S.age] * icu_overload_factor)
    icu_overload_factor: 
        if $(state=icu) <= max_icu_share: 1
        otherwise: (icu_overload_severity_factor * ($(state=icu) - max_icu_share) + max_icu_share) / $(state=icu)
    max_icu_share: icu_capacity / total_population
    icu_capacity:
        if day <= 121: 800 + 400 * (121 - day) / 121  #day 121 is June 30th
        otherwise: 800
    
