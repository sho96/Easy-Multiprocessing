import mp
import numpy as np
import os
import sys

# Running this will import all libraries that are imported to this main script
# This makes it unnecessary to write import statements at mp.process
mp.importLibraries(__file__) 


# This function requires numpy and os to run
def someHeavyFunction(x):
    print(np.__version__)
    print(os.cpu_count())
    a = 0
    for i in range(x):
        a += i
    return a


# With mp.importLibraries(__file__)
reuslts = mp.process(
    someHeavyFunction, 
    [
        (10000000, ),
        (10000000, ),
        (10000000, ),
        (10000000, ),
    ]
)


# Without mp.importLibraries(__file__)
reuslts = mp.process(
    someHeavyFunction, 
    [
        (10000000, ),
        (10000000, ),
        (10000000, ),
        (10000000, ),
    ],
    "import numpy as np\nimport os"
)

print(reuslts)
