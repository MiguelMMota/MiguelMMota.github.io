---
title: Looping fast in python II
description: ...and why I was the slowest in class at a trivial problem
date: 2021-04-02T00:17:00Z
tags: ["python", "fundamentals", "advanced"]
draft: true
---


 // TODO - intro

In a previous post 

## Intermediate

The next few strategies rely on a deeper mastery of some features of the Python language, such as built-in functions and multiprocessing as well as common third-party libraries that focus on speeding up and simplifying these sorts of tasks.

### Python built-ins
Python has a lot of handy built-in tools, which are often optimized for performance.

Here are a couple of solutions relying on the `sum` builtin function:

#### Built-in over a list

// TODO

```python
def sum_range_list_builtins(start, end):
    """
    Create a list of each integer in the interval [start, end], 
    and sum them up using the built-in method 'sum'
    """
    return sum(list(range(start,end))) 

print(t(sum_range_list_builtins))
```

// results

#### Built-in over a generator

// TODO

```python
def sum_range_generator_builtins(start, end):
    """
    Create a generator of each integer in the interval [start, end], 
    and sum them up using the built-in method 'sum'
    """
    return sum(range(start,end))

print(t(sum_range_generator_builtins))
```

// results
// Comment

### Third-party packages 

#### Pandas
[Pandas](https://pandas.pydata.org/docs/) is a very powerful library for data analysis in Python. Data can be structured in dataframes, which can be manipulated for tons of use cases with a large variety of methods. Dataframes are also handy for viewing data in a clean, structured format. For such a powerful library, it's also quite easy to pick up, though hard to master.

For our use case, it may seem a bit silly to resort to a dataframe. However, aggregating results in dataframe columns is not an uncommon task, so it would be useful to compare its performance against the alternatives.

```python
import pandas as pd

def sum_range_pandas(start: int, end: int) -> int:
    """
    Create a pandas dataframe with all the values in the integer interval [start, end] and return the column sum
    """
    result = 0

    return pd.DataFrame(range(start, end+1), columns=['value']).value.sum()

print(t(sum_range_pandas))
```   

// results

#### Numpy
[Numpy](https://numpy.org/) is a library tailored to mathematical operations in python with support for large arrays/matrixes of data. Let's see how it performs against the field:

```python
import numpy as np
def sum_range_numpy(start, end):
    """
    Return the sum of a numpy range representing the [start, end] interger interval
    """
    return np.arange(start, end+1).sum()

print(t(sum_range_numpy))
```

// results

## Multithreading
// Text

```python
import math
from threading import Thread


class ThreadWithReturnValue(Thread):
    """
    A subclass of Thread which returns the value of the target function
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None
        
    def run(self):
        if callable(self._target):            
            self._return = self._target(*self._args, **self._kwargs)
            
    def join(self, *args, **kwargs):
        Thread.join(self, *args, **kwargs)
        
        return self._return
    

def sum_range_multithreading(start, end):
    """
    Split the range into 8 equally sized segments and add each of them using the sum_range_generator_for_loop method.
    Return the sum of all ranges
    """
    num_threads = 8
    inc = math.ceil((end-start) / num_threads) 
    threads = [
        ThreadWithReturnValue(
            target=sum_range_generator_for_loop, 
            args=(
                start+ix*inc, 
                min(
                    start+(ix+1)*inc-1,
                    end
                )
            )
        )
        for ix in range(num_threads)
    ]
    
    for t in threads:
        t.start()
    
    return sum(t.join() for t in threads)

print(t(sum_range_multithreading))
```

## Advanced

// Text

### Numba
[Numba](http://numba.pydata.org/) is a *just-in-time* ([JIT](https://en.wikipedia.org/wiki/Just-in-time_compilation)) compiler that can make parts of your Python code much faster (on par with C++). You can apply it to your regular Python functions by using decorators, such as `@jit` and `@njit`.

Since the function is compiled the first time it's called, this will result in a much lower performance at this stage. However, subsequent calls are much faster. Numba is a fascinating project and would likely warrant its own post. If you want more information, check out this very nice example [video](https://www.youtube.com/watch?v=x58W9A2lnQc).

It's possible to decorate any Python function/method with the Numba JIT compiler, so technically we could retest all of our previous implementations this way. However, for the sake of demonstrating some of Numba's features and performance, I'll use a single implementation that is a bit of a compromise between the two.
// Explain implementation  

```python
## Numba
import math

from numba import njit, prange
import numpy as np


num_threads = 8

@njit()
def _sum_range(start, end):
    return np.arange(start, end+1).sum()

@njit(parallel=True)
def sum_range_numba(start, end):
    result = 0
    inc = math.ceil((end-start+1) / num_threads)
    
    for ii in prange(num_threads):
        s = start+inc*ii
        e = min(end, start+(inc+1)*ii-1)
        
        result = result + _sum_range(start+inc*ii, min(end, start+inc*(ii+1)-1))
        
    return result


# Run it once, to compile (which is slow), and only then measure performance
sum_range_numba(1, 100)
print(t(sum_range_numba))
```

// results

### Cython

// Text

### Pypy
> "If you want your code to run faster, you should probably just use PyPy."
> 
> \- Guido van Rossum *(creator of Python)*

...is what every Pypy fan will tell you. And it's true! Pypy is a [JIT](https://en.wikipedia.org/wiki/Just-in-time_compilation) compiler, which means that it compiles code at runtime. In the official project documentation it states that 

> "PyPy is a replacement for CPython"

This is because CPython compiles the Python code ahead-of-time ([AOT](https://en.wikipedia.org/wiki/Ahead-of-time_compilation), like in C/C++) into an intermediate bytecode that is then interpreted by a virtual machine. By compiling the code directly into assembly language, Pypy gets massive performance improvements in a large number of cases. 

Just like Numba, this can be a very large topic in its own right, so I'll defer you to one of many interesting PyCon [talks](https://www.youtube.com/watch?v=zQVytExlnEk) on the subject.
 
Setting up Pypy is similar to downloading and installing Python:

1. Download [here](https://www.pypy.org/download.html)
2. Move unzipped contents to the path of your choice
3. Add the root path and the `/Scripts` subfolder to the `Path` environment variable

Think of it as any other version of Python, so you can create virtual environments, install packages, all that good stuff. You can run any script just as before but with `pypy`/`pypy3` instead of `python`/`python3`.   

E.g.: `pypy3 my_script.py`

> **Tip:** You can also run jupyter notebooks with a Pypy kernel. Follow the instructions [here](https://stackoverflow.com/questions/33850577/is-it-possible-to-run-a-pypy-kernel-in-the-jupyter-notebook) to get started!

## And the winner is...

// TODO
[Carl Gauss](https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss) 
(n / 2)(first number + last number)


### How I was the slowest in class
// Previously named 'The tool for the task'


 