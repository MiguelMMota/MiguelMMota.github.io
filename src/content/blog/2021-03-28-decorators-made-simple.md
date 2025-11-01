---
title: Decorators made simple
date: 2021-03-28T00:17:00Z
tags: ["python", "fundamentals", "intermediate"]
draft: false
---


> "Great programmers learn how to program their tools, not just use them."
> 
> \- Steve Yegge

[Decorator syntax](https://www.python.org/dev/peps/pep-0318/) is a great tool in Python. Yet, newer programmers often struggle with the concept and settle for a superficial understanding of decorators, resulting in only superficially using them. The goal of this post is to break down the Python decorator, so we can use it to its full extent.

## What is a decorator?

Decorators are pythonic implementations of the [decorator design pattern](https://en.wikipedia.org/wiki/Decorator_pattern). Any object in Python can be used as a decorator, as long as it meets these three criteria:

- it's a *callable*
- it takes a *callable* as an argument
- it returns a *callable*
    
Easy, right?


### Hello, World!

Here's a very simple decorator:

```python
def print_hello_world(*args, **kwargs):
    print("Hello, World!")


def hello_world_decorator(func):
    return print_hello_world
```

Silly as this example is, `hello_world_decorator` is a valid decorator, as it checks the three necessary criteria:

- it's a *callable* (a function)
- it takes a *callable* as an argument (`func`)
- it returns a *callable* (`print_hello_world`)

We can use it to decorate any callable, like this:
```python
def some_func(value):
    pass


new_func = hello_world_decorator(some_func)
```

This snippet does three things:

1. define a function object and bind it to `some_func`
2. call `hello_world_decorator` with the earlier object as an argument, which returns the object referenced by `print_hello_world`
3. bind the output of the function call to `new_func`

Note that we could've bound the decorated function back to `some_func`, but we wanted to bind it to a new variable instead. Now, when we call `new_func`, we get "Hello, World!".


### Transforming a callable

In the previous example, the decorator wasn't actually very useful. We could achieve the same functionality with `new_func = print_hello_world`, while being much clearer (and shorter). In fact, our `hello_world_decorator` decorator is pointless: all it does is take in a callable, ignore it completely, and return some other callable. We're stretching the meaning of *transforming* the original callback, since we're merely disregarding it.

What if we wanted to add to our initial function instead? We need to find a way to run the original function whenever the decorated function is called. We can do this if decorated function is inside the decorator's scope.
Let's consider another example, where we want to create a decorator that prints a sentenec before a function is called:

```python
def print_before_decorator(func):
    def print_before(*args, **kwargs):
        print("I did not hit her, it's not true, it's bullsh*t! I did not hit her! *throws bottle* I did not...")
        return func(*args, **kwargs)
    return print_before
```

> **Tip:** The function defined inside the namespace of the decorator (`print_before` in this case) is often called `inner` or `wrapped`. Since it's defined in a local scope, there's no risk of overlapping with other decorators' own inner functions.

In this case, `print_before_decorator` is still a decorator: a *callable* that takes a *callable* (`func`) and returs a *callable* (`print_before`). In this case, we keep the functionality of the decorated callable by calling it in the inner function, after printing a string.

We can once again define and decorate a function with

```python
def say_hi(name):
    print(f"Oh, hi {name}!")


say_hi = print_before_decorator(say_hi)
```

Compare what this does with the previous example:

1. define a function object and bind it to `say_hi`
2. call `print_before_decorator` with the earlier object as an argument, which returns the object referenced by `print_before`
3. bind the output of the function call to `say_hi`

The differences are that now:

1. the returned function was defined inside the decorator scope (to have access to `func`)
2. the returned function returns the result of running `func`, to better emulate the functionality of `say_hi` 
3. the decorated function object is bound to `say_hi` instead of a new variable. We can test the result:

```python
say_hi(name="Mark")
I did not hit her, its not true, its bullsh*t! I did not hit her! *throws bottle* I did not...
Oh, hi Mark!
```

![](/2021-03-28-decorators-made-simple/oh_hi_mark.gif)

Perfect!

### Decorator syntax

A neat thing about Python is the shorthand for decorators. From the previous example:

```python
def say_hi(name):
    print(f"Oh, hi {name}!")


say_hi = print_before_decorator(say_hi)
``` 

is equivalent to:

```python
@print_before_decorator
def say_hi(name):
    print(f"Oh, hi {name}!")
``` 

This greately improves readability, as we avoid unnecessary references to objects (we write the function name only once, instead of three times), and the decorator is right on top of the function definition, making it easier to identify the transformations applied to our function just by looking up its definition.


### Nested decorators
The benefits of the decorator shorthand become more evident when we want to chain several decorators together. For example, if we're looking to keep track of when a callable starts and stops execution, we can create another decorator:

```python
from datetime import datetime


def track_execution(func):
    print("Track_execution")

    def inner(*args, **kwargs):
        print(f"Started at {datetime.now()}")
        result = func(*args, **kwargs)
        print(f"Finished at {datetime.now()}")

        return result

    return inner
```

What if we want to decorate `say_hi` with both `track_execution` and `print_before_decorator`?

```python
import time

@track_execution
@print_before_decorator
def say_hi(name):
    print(f"Oh, hi {name}!")
```

The decorators are applied from closest to farthest from the method definition, so this is the order of operations:

1. define a function object and bind it to `say_hi`
2. `print_before_decorator` decorates `say_hi`, returning `print_before`
3. `track_execution` decorates `print_before` (the output of the earlier decoration), returning `inner`

This is equivalent to:

```python
import time

def say_hi(name):
    print(f"Oh, hi {name}!")


say_hi = track_execution(print_before_decorator(say_hi))
```

The first option is much more readable to me.
This is the output of running `say_hi`:
```python
say_hi("Mark")
>>> Started at 2021-03-28 16:53:53.992581
>>> I did not hit her, it's not true, it's bullsh*t! I did not hit her! *throws bottle* I did not...
>>> Oh, hi Mark!
>>> Finished at 2021-03-28 16:53:53.992581
```


### Class decorators
Remember our initial definition for decorators: a *callable* that takes a *callable* and returs a *callable*. So far we've only seen how to create function decorators, but instances of classes that implement the `__call__` method are also callable. Let's rewrite `track_execution` as a class decorator:


```python
from datetime import datetime


class track_execution:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f"Started at {datetime.now()}")
        result = self.func(*args, **kwargs)
        print(f"Finished at {datetime.now()}")
    
        return result
```

Again, let's verify this implementation against the criteria for a decorator:

- it's a *callable* (any class can be called, implicitly running its `__new__` and `__init__` methods)
- it takes a *callable* as an argument (the `__init__` method that takes a single `func` argument)
- it returns a *callable* (a `track_execution` instance is callable, since the class implements the `__call__` method)

> **Note:** You may have noticed that I named my class `track_execution` instead of `TrackExecution`, against [PEP-8](https://www.python.org/dev/peps/pep-0008/) recommendations:

> "Almost without exception, class names use the CapWords convention.

This is one exception to that rule which I include in my style guide (I'll share this in a later post). In Python, classes that are most commonly used as functions are usually written in either *snake_case* (like functions) or at least in *lowercase*. 

Writing this decorator as a class is an implementation issue, which should be abstracted away at the user level. Otherwise, if the decorator were later changed into a function, the update would require fixing its usage everywhere in the codebase.

We can define and decorate our `say_hi` function with:

```python
import time


@track_execution()
def say_hi(name):
    print(f"Oh, hi {name}!")
```

Here's what this does:
1. define a function object and bind it to `say_hi`
2. call `track_execution` with the earlier object as an argument, which returns an instance of `track_execution` that has an attribute pointing to the object referenced by `say_hi` (`self.func`)
3. bind the `track_execution` instance object to `say_hi`


By the same token, note that the argument of the `__init__` method doesn't need to be a function, it could be any callable object.


### Going a bit deeper
Consider a more elaborate example. We want to make sure that `say_hi` works for group conversations where people are joining and leaving the group. When we `say_hi` to someone that wasn't in the conversation, we want to say *"Hi"*. When they leave the conversation, we want to say *"Bye"* to them instead. Since **every** class in Python is an object (and `function` is a class), we can manage attributes of a decorator's inner function.

```python
def alternate_greetings(func):
    def inner(name):
        if name in inner.people_greeted:
            print(f"Bye, {name}!")
            inner.people_greeted.remove(name)
        else:
            func(name)
            inner.people_greeted.add(name)

    inner.people_greeted = set()

    return inner


@alternate_greetings
def say_hi(name):
    print(f"Oh, hi {name}!")


say_hi(name="Mark")
>>> Bye, Mark!

say_hi(name="Mark")
>>> Oh, hi Mark!

say_hi(name="Megan")
>>> Bye, Megan!

say_hi(name="Megan")
>>> Oh, hi Megan!

say_hi(name="Mary")
>>> Oh, hi Mary!

say_hi(name="Mark")
>>> Bye, Mark!

say_hi(name="Mary")
>>> Bye, Mary!
```

The syntax for this use case with class decorators is perhaps a bit more intuitive:
  
```python
class alternate_greetings:
    def __init__(self, func):
        self.people_greeted = set()
        self.func = func
    
    def __call__(self, name):
        if name in self.people_greeted:
            print(f"Bye, {name}!")
            self.people_greeted.remove(name)
        else:
            self.func(name)
            self.people_greeted.add(name)
```

### One last tip

Let's look go back to the original decorator syntax, which we know to be equivalent to the `@` syntax, and consider a simple example:

```python
def print_name(func):
    """
    Decorate function, so its name is printed before it's called
    """
    def inner(*args, **kwargs):
        """
        Print func's name, then run it
        """
        print(f"Running {func.__name__}")
        return func(*args, **kwargs)
    return inner


def say_hi(name):
    """
    Say hi to someone
    """
    print(f"Oh, hi {name}!")
```

We can check the docstring for `say_hi` with

```python
say_hi.__doc__
>>> '\n    Say hi to someone\n    '
```

What happens when we decorate this function, though? Will `say_hi`.__doc__ return the docstring from `say_hi` (the original one), `print_name` or `inner`?
```python
say_hi = print_name(say_hi)
say_hi.__doc__
>>> "\n        Print func's name, then run it\n        "

say_hi
>>> <function __main__.print_name.<locals>.inner(*args, **kwargs)>

str(say_hi)
>>> '<function print_name.<locals>.inner at 0x0000026228500048>'
```

Recall that in the last step of decorating a function, the name of the original function references the objected returned by the decorator (which is the inner function, in this case).
It means that `say_hi` the original function object is no longer bound to `say_hi`, which now references the decorator's inner function.

With that in mind, we can understand why we lose the original function's documentation. Fortunately, there's a way around this: another decorator!

```python
from functools import wraps


def print_name(func):
    """
    Decorate function, so its name is printed before it's called
    """
    @wraps(func)
    def inner(*args, **kwargs):
        """
        Print func's name, then run it
        """
        print(f"Running {func.__name__}")
        return func(*args, **kwargs)
    return inner


@print_name
def say_hi(name):
    """
    Say hi to someone
    """
    print(f"Oh, hi {name}!")


say_hi
<function __main__.say_hi(name)>
say_hi.__doc__
'\n    Say hi to someone\n    '
str(say_hi)
'<function say_hi at 0x00000262284FF708>'
``` 

> **Note:** You may have noticed that the `@wraps` decorator doesn't look exactly like the ones we covered so far, since it takes a parameter (`func`). Check out [this useful resource](https://www.geeksforgeeks.org/decorators-with-parameters-in-python/) if you want to know more about decorators with parameters!

As we can see, this decorator allows us to keep the information about the original function after decorating it. Essentially, it decorates the `inner` function, overwriting its name, module, and docstring with the corresponding values from the original callable.


So that's it! I hope this post helped you gain a better understanding of decorators and how to use them better!
