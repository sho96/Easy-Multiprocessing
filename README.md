# pythonicMultiprocessing
No need for writing __name__ == "__main__" for multiprocessing
## How to use
### Basics
* Import mp.py file into your script by 
```python
import mp
```
* Defile a function you want to run with multiple CPU cores <br>
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
results = mp.process(function, [(100, 200), (200, 300), (300, 400)])
print(results)
```

### Using other libraries with functions run on mp.process()
* Calling mp.importLibraries anywhere before mp.process()
```python
mp.importLibraries(__file__)
```

This will import all libraries to the functions that will be run with mp.process() <br>
Notice: However, importing unnecessary libraries can lead to increasing RAM usage
* Specifying 'imports' argunment for for mp.process()
```python
mp.process(
    function,
    [("a","r","g","s","1"), ("a","r","g","s","2")], 
    imports = """
    import numpy as np
    import sys
    """
)
```
This can prevent increasing RAM usage caused by mp.importLibraries at the cost of writing more code