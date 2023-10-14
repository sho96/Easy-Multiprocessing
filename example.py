import mp

mp.importLibraries(__file__) 


def someHeavyFunction(x):
    a = 0
    for i in range(x):
        a += i
    return a


reuslts = mp.process(
    someHeavyFunction, 
    [
        (10000000, ),
        (10000000, ),
        (10000000, ),
        (10000000, ),
    ]
)

print(reuslts)
