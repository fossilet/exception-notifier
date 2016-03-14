# exception-notifier [![Build Status](https://travis-ci.org/fossilet/exception-notifier.png?branch=master)](https://travis-ci.org/fossilet/exception-notifier)  [![Coverage Status](https://coveralls.io/repos/fossilet/exception-notifier/badge.png?branch=master)](https://coveralls.io/r/fossilet/exception-notifier?branch=master)

Notify uncaught exceptions in your Python code.

This module works with Python 2.7, 3.5 and PyPy.

## Installation

Exception Notifier is available at
[PYPI](https://pypi.python.org/pypi/exception-notifier),
you can install it using `pip`:

    pip install exception-notifier

Or you can clone the repo and run:

    python setup.py install

## Usage

### Override default exception hook

The simplest usage:

```python
import exception_notifier as en
en.enable()
```

After this, all uncaught execptions will be mailed to your local account
(provided you have a local mail server). `enable` can be customized with the
same arguments with `mail_exception` as showed below.

If you want to restore to the default hook, use:

```python
en.disable()
```

### Handling individual function

Use the `mail_exception` function to return an decorator for your function.
Then every uncaught exception in your function will be mailed to you.

```python
from exception_notifier import mail_exception

exception_notifier_conf = {
    'sender': 'tux@localhost',
    'receivers': ['tux@localhost'],
    'mail_server': 'localhost',
}

@mail_exception(**exception_notifier_conf)
def fancy_function():
    ...
```

You may better wrap your whole module in a starting script. Thus not only
functions, but every line in your module will be protected by
exception-notifier. Your module `fancy_module` may look like this:

```python
def func1():
    ...

def func2():
    ...

def main():
    func1()
    func2()
```

Your wrapper scripts may look like this:

```python
from exception_notifier import mail_exception

exception_notifier_conf = {
    'sender': 'tux@localhost',
    'receivers': ['tux@localhost'],
    'mail_server': 'localhost',
}


@mail_exception(**exception_notifier_conf)
def main():
    import fancy_module
    fancy_module.main()

if __name__ == '__main__':
    main()
```

This way you will be notified if any line in your module raises an uncaught
exception.

### Use custom callback

If you want to use custom callback function instead of the default behavior
of sending email, you can use the callback argument like below:

```python
@mail_exception(callback=f, args=(1, 2),
    kwargs={'x': 3}, **exception_notifier_conf)
```

If the argument `both` is True, then not only the mail is sent, but the
callback function is executed also.

In the callback function, you probably want to deal with the exception
information, then [sys.exc_info()](http://docs.python.org/2/library/sys.html#sys.exc_info) is conveniently at your service.

## Bugs

There is no way to get the return value of `callback` in Python code,
so the return value of it is meaningless, even if you can return some value
explicitly in it.

The coverage reported by Coveralls is inaccurate because Travis cannot run
code sending email. Run tests/test_coverage.sh to get a full coverage.
However, `python-coverage` does not cover code of system exception hook
in either case.

## Thanks

Powered by PyCharm under an [Open Source License](http://www.jetbrains.com/pycharm/buy/buy.jsp#openSource).
