Dynamod - model specification reference
=======================================

###Table of Contents

- [overall document structure](#overall-document-structure)
- model sections:
  - [attributes](#attributes)
  - [progressions](#progressions)
  - [parameters](#parameters)
  - [formulas](#formulas)
  - [extends](#extends)
- [expressions](#expressions)
- [grammar](#grammar)


## Overall Document Structure
<a name="overall-document-structure"></a>
Dynamod models are written in a formal model description language. The overall syntax of model files follows roughly the concept of Python programs, i.e.:

- Comments can appear everywhere, everything after '#' is treated as comment
- indentation defines the scope of operations or expressions. Indentation can be defined by spaces or tabs (but do not mix them!)
- basic syntax for calculations, comparisons, lists etc.

Model files consist of up to five sections, a minimal model needs two of them. The sections are:

## attributes
<a name="attributes"></a>

Each attribute partitions the population into groups, corresponding to the different values of the attribute. A classical SIR model for example only uses one attribute, the infection state, with values susceptible, infected and recovered. You can define as many attributes as you like, like age, risk group, type of virus, vaccination state etc. For each attribute, you enumerate the possible values and their initial shares in the population. The initial share of one attribute's values can depend on the value of other attributes. The set of all attributes partitions the population into a multi-dimensional space of value combinations.

To describe initial shares, you have three options: 
- list: just a list of numbers, one for each value, that add up to 1
- dependent list: multiple lists, split over other attribute's values
- map of entries value: share, where share can be split over other attribute's values

You can see all three variants in the following example:

```
attributes:

  age:
    values: [kid, adult, old]
    shares: [25%, 60%, 15%]       # shares as a simple list. Notations 1.5%, 0.015 and 1.5E-2 are all equivalent
    
  state:
    values: [susceptible, exposed, recovered]
    shares: 
        for age=kid:  [99.9%, 0.1%, 0]    # state share depend on age
        for age=adult:  [%%, 0.2%, 0.3%]  # Notation '%%' means 'rest to get 100%'
        for age=old:  [%%, 0.1%, 0.15%]
        
  risk:
    values: [low, medium, high]
    shares:
        high:
            for age=kid: 5%
            for age=adult: 10%
            for age=old: 30%
        medium:
            for age=kid: 30%
            for age=adult: 50%
            for age=old: 70%
        low: %%
```

## progressions
<a name="progressions"></a>

Each progression describes a process that leads to a change of one or more attribute values. In the classic SIR model, there are only two transitions: the infection (changing infection state from susceptible to infected) and the recovery (changing the state from infected to recovered). You can define as many progressions as needed to adequately describe your model's dynamic.

Each progression tells Dynamod what to change and on which segment of the population to change it. What to change is just a series of assignments of the form set attribute=value. For the question on which segment these changes are to be applied, Dynamod has several building blocks. These are:

- segment restrictions: `for <attribute>=<value>: …`
- segment list restrictions: `for <attribute> in [<value1>, <value2>, …]: …`
- operation share/probability: `for <share>: …`
- conditional operation: `if <condition>: …`
- the 'otherwise' restriction (if none of the above applies): `otherwise: …`
- the after-operations: `after.xxx(..): …`

These building blocks can be nested to define fine-grained segments of the population where a certain change should occur. On the same level, however, you can only split the population along one single attribute. This last requirement guarantees that all segments within a single progression are mutually exclusive. Therefore, it is clear which operation will be applied to a given attribute combination.

```
progressions:        
    an_example:
        for state=exposed:
            for 10%:
                set state=symptomatic
                for risk=high:
                    for 40%:
                        set hospitalized=yes
                for risk=low:
                    for 10%:
                        set hospitalized=yes
                otherwise:
                    for 20%:
                        set hospitalized=yes
```

Operations within a progression can be considered to be applied simultaneously: they don't interfere with each other since they operate on non-overlapping segments. On the other hand, different progressions are applied one after another in the sequence they are written in. 

The after-operations perform the changes not on some explicit percentage of the selected segment, but after a certain time (in ticks). Depending on the after-type the distribution of the transition time can be modelled. There are currently three ways to express the distribution (other distributions can be added as needed):

- `after.fix(x)`: 100% will be taken after exactly x ticks. If x is not an integer, two ticks are mixed (e.g. with after.fix(3.2) will happen on tick three for 80% of the segment and on tick four for 20%)
- `after.std(x,s)`: a standard distribution with mean x and deviation s is mapped to time units
- `after.explicit(x1,x2,x3,…)`: a share of x1 will be taken on tick 1, a share of x2 on tick 2 etc., the sum of all xi being 1

The delay count for the after-operations starts at 0 in the iteration where the segment is "entered" by another progression. Since after-operations do not start before delay 1, a segment will not be entered and left during the same iteration. The history of "entering" into the segment before the start of iterations cannot be stated explicitly yet. It is deduced by the initial share of the segment and the delay distribution, so that a) it will decrease to zero if no further influx into the segment happens and b) the influx was assumed as constant on each iteration before 0.

##parameters
<a name="parameters"></a>
The parameter section defines numeric parameters, which are just numbers with a name. The number given in the model is the default, but the parameter value can be modified "from outside" when the model is calculated or calibrated.

##formulas
<a name="formulas"></a>
The formula section defines values and/or functions that can be used in progressions, results or other formulas. They are recalculated on demand in each iteration.
While local variables can be defined on the spot inside of progressions, the use of formulas is preferred, since the offer a couple of advantages:
- they can be reused
- they can be nested (i.e. using one formula inside another one), simplifying and structuring the calculations
- they can have parameters
- they offer extension points to build upon the model (see later)

##results
<a name="results"></a>
The results section can contain any number of specific result values. Each result entry is calculated at each iteration and leads to a time series of result values. These results can later be retrieved as arrays (for a single result) or pandas DataFrames (for multiple results).
The distribution of attribute values doesn't have to be listed in the results section. Time series for these distributions are automatically recorded and available after the model has run.

##extends
<a name="extends"></a>
In Dynamod, models can be extended by other models. To extend a model, the extension line:
```
extends: '<base model path>'
```   

must be the first line in the model description. Any named objects (attributes, progressions, parameters, formulas and results in the extension model are added to the base model, possibly replacing any existing object of the same name.
Since the order of progressions is relevant (they are performen one after another), it is possible to insert a new progression at a specific point into the base model's progression list by using the notation:

```
progressions:        
    my_new_progression at existing_progression:
```

Without this explicit positioning, new progressions are appended at the end of the existing ones.

##Expressions
<a name="expressions"></a>
Normal Python-like expressions are available in Dynamod:

- calculations (`+, -, *, /, **`)
- comparisons (`<, <=, >, >=, !=`)
- logical (`and, or, not`)
- numbers (`123, 12.3, 1.2E3, 12%`)
- local variable definition (definition by assignment)
- object member access (`x.y`)
- object method access (`x.y(…)`)
- strings (limited by single or double quotes)
- access of local variables, parameters and formulas (by name)
- Python-style conditional expressions: `<x> if <cond> else <y>`

Objects can be inserted into Dynamod's namespace when initializing the model. There are two predefined variables:

- **ALL**: the total population, which is a starting point for population segments (see below)
- **day** (or **time**): both refer to the iteration tick count, starting at 0

For top-level expressions like formulas or local variables, a split syntax over population attributes can be used:

```
formulas:        
    my_formula:
        for risk=high:
            #something here
        for risk=low:
            #something else
        otherwise:
            #something completely different
```

A special notation is available to describe population segments. There are several ways for this:

- the predefined variable `ALL` (the total population with no restrictions)
- `attribute=value` (the population segment having the given value for the given attribute
- `attribute in [value1, value2, …]` (the population segment having one of the listed values for the given attribute
- if `X` is a population segment, `X with attribute=value` is another one (further restricting the segment)
- if `X` is a population segment, `X with attribute in [value1, value2, …]` is another one (further restricting the segment)
- if `X` is a population segment, `X.before(D)` is another one, denoting the population segment `D` days earlier. `D` must be an integer value. If `D` is greater than the current iteration count, `X` is returned

Population segments are primarily used to calculate absolute or relative population shares. If `X` and `Y` are population segments,

- `$(X)` returns the (absolute) share of segment `X` in the population
- `$(X|Y)` returns the relative share of `X` within `Y`

## grammar
<a name="grammar"></a>
The complete formal grammar for Dynamod models can be found [here](dynamod/parser/Dynamod.g4). 