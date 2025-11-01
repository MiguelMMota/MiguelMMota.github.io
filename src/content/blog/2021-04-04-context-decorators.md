---
title: Context decorators
description: Using an object as both a context manager and a decorator
date: 2021-04-04T00:17:00Z
tags: ["python", "fundamentals", "intermediate"]
draft: false
---

[Context managers](https://www.python.org/dev/peps/pep-0343/) and [decorators](https://www.python.org/dev/peps/pep-0318/) are widely used constructs in the Python language that allow us to dynamically alter the functionality of our code in a limited scope. The use cases for these are often different, but what happens when we want our class to be usable as both a context manager and a decorator?

![](/2021-04-04-context-decorators/porque_no_los_dos.png)

Enter the [context decorator](https://docs.python.org/3/library/contextlib.html#contextlib.ContextDecorator). By the way, you can check out some example code for this post [here](https://gitlab.com/miguel_mota/miguel_mota.gitlab.io/-/blob/master/src/2021-05-02-looping-fast-in-python/code.ipynb). 

Let's do some recap: 

## Decorators

A decorator is used to transform a *callable*, and meets three criteria:

1. it's a *callable*
2. it takes a *callable* as an argument 
3. it returns a *callable*

They can be implemented as such:
 
 ```python
def decorator_name(func):
    def inner(*args, **kwargs):
        ...
        result = func(*args, **kwargs)
        ...

        return result
    return inner


@decorator_name
def some_func(*args, **kwargs):
    ...
```

> **Note:** Although this template is common for most decorators, it's merely a common pattern of implementation. In reality, **any** object that meets the three criteria listed above can be used as a decorator.

Check out my [earlier post](/blog/2021-03-28-decorators-made-simple) for a detailed overview of decorators.

 
## Context managers
It's likely that you've used context managers before, even if you weren't aware of it. Anything that can be used with the `with` keyword in Python is a context manager. 

This design pattern is often used for handling setup and teardown operations within a limited scope, such as file, connection and lock handling. Consider the example of handling [critical sections](https://en.wikipedia.org/wiki/Critical_section) in Python threads. We have a `shared_counter` variable that is incremented concurrently by multiple threads:

```python
# Without context manager
import time
from threading import Lock, Thread

MAX_THREADS = 6
shared_counter = 0
lock = Lock()

def add_to_counter(num_iterations):
    global shared_counter
    
    for _ in range(num_iterations):
        lock.acquire()
        new_value = shared_counter + 1
        time.sleep(0.01)
        shared_counter = new_value
        lock.release()


def count_concurrently(num_iterations):
    global shared_counter
    shared_counter = 0
    
    threads = []
    for ix in range(MAX_THREADS):
        t = Thread(target=add_to_counter, args=(num_iterations,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


    print(f"Final value: {shared_counter} (expected {int(num_iterations*MAX_THREADS)})")
    
    
count_concurrently(num_iterations=100)
>>> Final value: 600 (expected 600)
```

We'll leave concurrency as a topic for another post...for now, it's sufficient that we understand that the lock allows us to make sure that after a thread has read the `shared_counter` value, no other threads will access that same block of code until the original thread has finished updating the variable.

This is a very common use case for locks:

1. Acquire lock
2. Do some logic
3. Release lock

, which in Python can be simplified with a context manager:

```python
# Don't do this
lock.acquire()
count_concurrently()
lock.release()

# Do this
with lock:
    count_concurrently()
``` 

There's a few reasons for using context managers in situations like this:

- It removes the need for boilerplate code, making it shorter, and more readable
- It abstracts implementation from business logic
- It allows for resources to be freed even if execution fails within the scope
- It facilitates error handling (by handling expected errors in the `__exit__` method)
- It prevents silly mistakes, such as forgetting to release the lock (or closing files/connections)
 
Check out this [great talk](https://www.youtube.com/watch?v=wf-BqAjZb8M) that showcases how leveraging context managers can be an easy way to make your code more pythonic.

### Creating a context manager
The `Lock` class from the previous example was designed to be used as a context manager. Any class can have this behaviour enabled by defining its `__enter__` and `__exit__` dunder methods.

Let's create our own context manager to time the operation of our `count_concurrently` function. First, let's see what a possible solution would look like without a context manager:

```python
import time


print("Tracking execution time: ")
start_time = time.time()

count_concurrently(num_iterations=100)

end_time = time.time()
print(f"Finished. Took {start_time - end_time:.2f} seconds")
```

We don't have to have to dig up our code like that when we're testing it, mixing internal logic with this timing implementation. I much prefer defining a separate class or function to time the execution, which can later be reused for any other part of the codebase:

```python
import time


class timer:
    start_time = time.time()

    def __enter__(self):
        print("Tracking execution time: ")
        self.start_time = time.time()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        print(f"Finished. Took {end_time-self.start_time:.2f} seconds")
        self.start_time = None


with timer():
    count_concurrently()
```

> **Note:** A few interesting points to mention:

- Here, the `__exit__` method gets a few extra parameters (exception type, value, and traceback) to handle exceptions that may occur inside the context manager
- instances of `timer` can be used as context managers, not the class itself, so we're instantiating it.
- the `__enter__` method should return or yield an object. The `with` keyword can be used to alias this output to be used within the context. A frequent example of this is when managing files:
```python
with open(filepath, 'r') as f:
    f.readlines()
```

### Context managers as functions
We can implement context managers as functions by following two steps:

1. decorating the function with `@contextlib.contextmanager`
2. making the function a [generator](https://python-reference.readthedocs.io/en/latest/docs/generator/), by adding a `yield` statement to the function body.

Our `timer` context manager could be re-written as:
```python
from contextlib import contextmanager
import time


@contextmanager
def timer():
    print("Tracking execution time: ")
    start_time = time.time()
    
    yield
    
    end_time = time.time()
    print(f"Finished. Took {end_time-start_time:.2f} seconds")


with timer():
    count_concurrently(num_iterations=100)
```

Checkout [this article](https://book.pythontips.com/en/latest/context_managers.html#implementing-a-context-manager-as-a-generator) for more info on this

## Context decorators

Now that we've covered decorators and context managers separately, all that's left is fusing the two together.

![](/2021-04-04-context-decorators/fusion.jpg)
*(Ok, maybe I had a bit too much fun with this one)*

In true Python fashion, this couldn't be easier to implement: 

- context manager function: no need to change anything, the `contextlib.contextmanager` decorator already turns the function into a context decorator. 
- context manager class: we just need to make the class inherit from `contextlib.ContextDecorator`:

```python
from contextlib import ContextDecorator
import time


class timer(ContextDecorator):
    start_time = time.time()

    def __enter__(self):
        print("Tracking execution time: ")
        self.start_time = time.time()

        yield self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        print(f"Finished. Took {self.start_time - end_time:.2f} seconds")
        self.start_time = None
```

Now our `count_concurrently` function can be decorated:

```python
@timer()
def count_concurrently():
    ...     
```

Remember that now `timer` can be used both as a decorator and as a context manager. A benefit of this is that the context decorator can be used to either transform callables at definition or altering them when they're called. 

> **Note:** Another neat perk of both `contextmanager` and `ContextDecorator` (when used as decorators) is that they use `functools.wraps` to keep the original function's information such as name, module, and docstring.

## A use case
Our `timer` class isn't actually very useful, since there are builtins for this sort of thing, such as the [timeit](https://docs.python.org/3/library/timeit.html) module. Here's another tool we can use to help us analyse our code efficiency:

```python
from contextlib import contextmanager
import cProfile
from pstats import Stats


@contextmanager
def profile():
    with cProfile.Profile() as pr:
        yield
        
    stats = Stats(pr).sort_stats('cumulative')
    stats.print_stats()
```


This context decorator ensures that whatever code is run within its context is profiled with `cProfile.Profile()`, then prints some statistics. For example:

```python
with profile():
    count_concurrently(num_iterations=100)
``` 

yields the following results:

```
Final value: 600 (expected 600)
         317 function calls in 10.054 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   10.054   10.054 <ipython-input-45-caa3345a10c6>:2(count_concurrently)
       33   10.040    0.304   10.040    0.304 {method 'acquire' of '_thread.lock' objects}
```

The lines are sorted by `cumtime`, and there's a lot more lines below it tracking operations in submodules, showing only the top 2 for brevity. In more complex systems, this has shown to be an invaluable tool.

So there you have it! If you understand decorators and context managers, context decorators are a very small step further, and they can be a great way to make your internal tools a lot more flexible and powerful!