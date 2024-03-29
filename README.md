﻿# Easy Multiprocessing
Multiprocess without \_\_name\_\_ == "\_\_main\_\_"<br>
All you need is mp.process()
# How to use
## Basics
* Import mp.py file into your script by
```python
import mp
```
* Define a function you want to run with multiple CPU cores <br>
Example: 
```python
def function(x, y):
    a = 0
    for i in range(x):
        a += i
    return a + y
```
* Run the function using mp.process
```python
results = mp.process(
    function, 
    [(100, 200), (200, 300), (300, 400)]
)
print(results)
```

## Using libraries on mp.process()
* Calling mp.importLibraries anywhere before mp.process()
```python
mp.importLibraries(__file__)
```
This will import all libraries imported on the running script to the functions that will be run with mp.process() <br>
Notice: However, importing all libraries that might have unnecessary libraries for running the function could lead to increasing RAM usage

* Specifying 'imports' argument for mp.process()
```python
results = mp.process(
    processImg, 
    [(100, 200), (200, 300), (300, 400)],
    imports="""
    import numpy as np
    import cv2
    """
)
print(results)
```
With this approach, you can prevent the imports of unnecessary libraries.<br>
Thus preventing the increasing RAM usage

## You might want to know ...
* You can use function decorators like numba.jit<br>
Example:
```python
import mp
from numba import jit

mp.importLibraries(__file__)

@jit(nopython=True)
def heavyFunction(arg1):
    #Do something heavy
    return result

results = mp.process(heavyFunction, [100, 200, 300])
print(results)
```
Note that jit still compiles the function every time mp.process is called.<br>
Functions need to be heavy enough for jit to be effective
