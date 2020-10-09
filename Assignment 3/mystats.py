'''
Team 12
Evan Kramer
evankram

Chase Pasciuto
cpasciut
'''

# File: mystats.py
import numpy as np

# define the mean function here
def is_iter(v):
    is_iter = True
    try:
        iter(v)
    except:
        is_iter = False
    return is_iter

def mean(*args):
    numerator = 0
    denominator = 0    
    for arg in args:
        denominator += len(arg) if is_iter(arg) == True else 1
        numerator += sum(arg) if is_iter(arg) == True else float(arg)
    return numerator / denominator       
        
# define the stddev function here
def stddev(*args):
    m = []
    for arg in args:
        if is_iter(arg) == True: 
            for a in arg: 
                if type(a) in [int, float, np.float64]:
                    m.append(a)
                else:
                    print('Please enter a valid set of numbers')
        elif type(arg) in [int, float, np.float64]:
            m.append(arg)
        else:
            print('Please enter a valid set of numbers')
    m = np.array(m)
    avg = mean(m) 
    return (np.sum((m - avg)**2) / (len(m) - 1))**(1/2)    

# define the median function here
def median(*args):
    m = []
    for arg in args:
        if is_iter(arg) == True:
            for a in arg:
                if type(a) in [int, float, np.float64]:
                    m.append(a)
                else:
                    print('Please enter a valid set of numbers')
        elif type(arg) in [int, float, np.float64]:
            m.append(arg)
        else:
            print('Please enter a valid set of numbers')
    
    m.sort()
    if len(m) % 2 == 1:
        n = m[len(m) // 2] 
    else:
        n = (m[len(m) // 2 - 1] + m[len(m) // 2]) / 2
    return n
    
# define the mode function here
def mode(*args):
    m = []
    for arg in args:
        if is_iter(arg) == True:
            for a in arg:
                if type(a) in [int, float, np.float64]:
                    m.append(a)
                else:
                    print('Please enter a valid set of numbers')
        elif type(arg) in [int, float]:
            m.append(arg)
        else:
            print('Please enter a valid set of numbers')
    # d = np.unique(m)
    d = {i: m.count(i) for i in np.unique(m)}
    return tuple(key for key, value in d.items() if value == max(d.values()))

# part (a)
print('The current module is:', __name__)
# Output: 'The current module is: __main__

if __name__ == '__main__':
    
    # part (b)
    print('mean(1) should be 1.0, and is:', mean(1))
    print('mean(1,2,3,4) should be 2.5, and is:',
                                        mean(1,2,3,4))
    print('mean(2.4,3.1) should be 2.75, and is:',
                                        mean(2.4,3.1))
    # print('mean() should FAIL:', mean())
    
    # part (c)
    print('mean([1,1,1,2]) should be 1.25, and is:',
                                    mean([1,1,1,2]))
    print('mean((1,), 2, 3, [4,6]) should be 3.2,' +
          'and is:', mean((1,), 2, 3, [4,6]))
    
    # part (d)
    for i in range(10):
        print("Draw", i, "from Norm(0,1):", np.random.randn())
    # List comprehension and mean of 50 draws
    ls50 = [np.random.randn() for i in range(50)]
    print("Mean of", len(ls50), "values from Norm(0,1):", mean(ls50))
    # List comprehension and mean of 10000 draws
    ls10000 = [np.random.randn() for i in range(10000)]
    print("Mean of", len(ls10000), "values from " + "Norm(0,1):", mean(ls10000))
    
    # part (e)
    np.random.seed(0)
    a1 = np.random.randn(10)
    print("a1:", a1)    # should display an ndarray of 10 values
    print("the mean of a1 is:", mean(a1)) # should be 0.7380231707288347
    
    # part (f)
    print("the stddev of a1 is:", stddev(a1)) # should be 1.0193909949356386
    
    # part (g)
    print("the median of a1 is:", median(a1)) # should be 0.6803434597319808
    print("median(3, 1, 5, 9, 2):", median(3, 1, 5, 9, 2))
    
    # part (h)
    print("mode(1, 2, (1, 3), 3, [1, 3, 4]) is:", mode(1, 2, (1, 3), 3, [1, 3, 4]))
else:
    pass