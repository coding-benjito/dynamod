Dynamod - User Guide
====================

Once the formal model specification has been written (see [the model reference](MODEL_REFERENCE.md)), the model can be calculated. A minimal Python setup can be seen in this example:

```
from dynamod.model import *
import matplotlib.pyplot as plt

model = parse_model('example.mod')
model.initialize()
model.run(300)
df = model.get_attributes('state')
df.plot()
plt.show()
```

In this example, the model file is parsed, initialized with default parameters, and then run for 300 iterations.

After the model has been calculated, the time series of the various `state` attribute values is extracted as a pandas DataFrame and plotted.

## Parsing the model

`parse_model(srcfile)` reads the model description file, applies the Dynamod grammar and returns the compiled dynamic model. Once a model has been parsed, it can be initialized and run several times.

Should parsing fail, the parser will output a problem description and terminate. In this case, it can be helpful to include the optional parameter `parse_model(srcfile, trace=True)` in order to see the token stream and parser actions leading to the problem reported.     

## Initializing

`model.initialize(parameters=None, objects=None)` must be called on the model before it can be run. As optional invocation parameters you can specify:

- `parameters`: a dictionary mapping parameter names to values, overriding the initial values in the model's `parameters:` section
- `objects`: a dictionary mapping names to user supplied Python objects, which are inserted into the model's namespace and can be used in expressions

After a model has been run, you must repeat the initialization before running it again.

## Running the model

`model.run(cycles, trace_at=None)` is used to calculate the model for the given number of iterations. To debug the model, set the `trace_at` parameter to the iteration number you want to analyze. During this iteration, the calculation details of all expressions will be output to the console. 

## Retrieving results

After the model has been run, there are two kind of results available: 

- attribute values: for each attribute and value, the share of the population having this value is available as a time series.
- user defined results: each named result in the model's `results:` section can be retrieved as a time series

In general, if a single (one-dimensional) result is requested, it is returned as a numpy array of floats. If multiple results are requested, they are returned as a pandas DataFrame. All result retrieval methods have optional `start=...` and `stop=...` parameters. These can be used to slice the time series arrays. As usual, the `start` index will be inclusive, the `stop` index exclusive. If neither `start` nor `stop` is given, the complete time series is returned.

These are the methods available to retrieve results:

```
model.get_attribute(attribute, value, start=None, stop=None): returns the share having the given value for the given attribute  
model.get_attributes(attribute, start=None, stop=None): returns the shares for all the attribute's values 
model.get_result(name, start=None, stop=None): returns the named result
model.get_results(names, start=None, stop=None): returns all named results (names is an iterable)
model.get_all_results(start=None, stop=None): returns all named results
```

Attribute value shares can be included in `get_results()` by specifying their name as "attribute=value".

## Calibrating the model

Models can be calibrated by automtic parameter fitting. In this process, a specific set of parameters are varied, so that model results are close to their expected values. Specifically, they are varied to find a minimum for a specified error metric measuring the difference between expected and actual results.

Dynamod uses the gradient descent algorithms of the Python package [gradescent](https://github.com/andromed2/gradescent). The basic idea of this algorithm:

1. Find a starting point: this can be the parameters' default values, or multiple starting points are evaluated by means of a grid search. Using a grid search approach increases the chance to find a global minimum instead of just a local one. If multiple parameters use the grid search, a multi-dimensional grid of initial values is evaluated. Grid search will of course greatly increase the calibration time.
2. Estimate the gradient at this point: by increasing each parameter value by a little dx, the change in the (error) result is recorded. The vector of all the relative changes (dy/dx) is an approximation of the gradient at this point. The negative of this gradient is the fastest way towards lesser error.
3. Find a step size to move along the negative gradient. A backtracking line search algorithm using Armijo conditions is applied for this. 
4. Move the current point by this step.
5. Repeat until the maximum number of iterations is reached or no reasonable improvements are made.

For the practical process of calibration, you create a Calibration object, add a number of parameters that can be modified, add a number of targets (expected model outcomes), and finally run the calibration process.

### Creating a Calibration object

```
cal = Calibration(model, cycles)
```
You pass the model (i.e. the result of the parse_model() call) and the number of cycles (e.g. days) the model should be run for each calibration step.

### Add modifiable parameters

```
cal.add_variable(name, min=None, max=None, grid=None, integral=False, dx=None)
```
- `name`: a parameter name included in the `parameters:` section of the model description
- `min/max`: limits to the allowable parameter values, if needed
- `grid`: if specified, `min` and `max` values are also needed. The interval between them is divided into `grid` equal parts, the middle of each of these sub-intervals is one starting point for the grid search. If `grid` is not specified, the model's default value is the starting point for the parameter.
- `integral`: if set to `True`, this parameter can only have integer (integral) values (e.g. days)
- `dx`: if given, determines the step size for the gradient calculation. If missing, 1/1000 of the initial value is used (if the initial value is 0, `dx` must be specified) .

### Add calibration targets

```
cal.add_target(resultname, expected, type='values', start=0, stop=None, weight=1, metric='mean_absolute_error'):
```
- `resultname`: the name of a result included in the `results:` section of the model description, or an attribute value share of the form 'attribute=value'
- `expected`: the expected outcome of the result. This can be an array of same length as the result time series, or a single constant value for the whole time 
- `type`: how the expected outcome is described:
  - `type='values'`: the result's time series (possibly restricted by start/stop) should match the array (or constant value) given by the `expected` parameter
  - `type='min'` or `'max'`: the minimum or maximum value of the result's time series, which should match the (single) value of the `expected` parameter 
  - `type='tmin'` or `'tmax'`: the time when the minimal or maximal value is reached, which should match the (single) value of the `expected` parameter. If the time series is restricted by `start/stop` parameters, the time will be relative to the start point, not the absolute model iteration time. 
- `start/stop`: a possible restriction to slice the result's time series values.
- `weight`: the weight factor to multiply this error term with, before multiple targets are summed up
- `metric`: how the difference between expected and actual values are measured. Possible values are 'mean_absolute_error', 'mean_squared_error', 'max_absolute_error' and 'median_absolute_error'
   
### Perform the calibration

Unfortunately, calibration is more art than science. The dependency between the parameters and the results varies wildly, and so some tweaking of the calibration parameters can be necessary. Therefore, the trace-Parameter is set to True by default to allow you to inspect the calibration progress. If the error diminishes steadly (and ideally approaches zero), everything is fine. If not, in trace mode you can probably see what goes wrong: too big or too small steps, focussing on bad local minima, slow convergence etc. In these cases, play around with some of the optimization's parameters and see how the iterations change.

```
cal.optimize(zoom_limit=1e6, momentum=0, iterations=100, min_improvement=0.0001, trace=True, debug=False):
```
- `zoom_limit`: near the end of the calibration, only small steps and small improvements can be made. In this situation, the dx-parameters to calculate the gradient may become too large. An automatic "zoom-in" process reduces the dx values for the final fine-tuning. The value of the zoom_limit parameter controls the amount of zooming that will be performed.  
- `momentum`: if standard convergence is too slow, increase the momentum value. This adds part of the step (direction and length) of the previous improvement to this iteration.  
- `iterations`: the number of improvement cycles the calibration will perform
- `min_improvement`: the total error term must decrease by at least this amount on each iteration, otherwise the calibration will be stopped 
- `trace`: print some diagnostic output on each iteration
- `debug`: if True, print even more diagnostic output
   
The return value of cal.optimize() is a 2-tupel: the first component is a dictionary mapping parameter names to their found optimum values, the second component is the error term reached with these parameter values.
