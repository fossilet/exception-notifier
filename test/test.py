#! /usr/bin/env python

"""Test script.


Test mail function and custom callback function.
>>> f(1,0)
-----
type: <type 'exceptions.ZeroDivisionError'>
value: integer division or modulo by zero
-----
"""

import sys

# Must run from the project root.
sys.path.insert(0, '.')
import exception_notifier


def exc_handler():
    typ, value = sys.exc_info()[:2]
    print '-----'
    print 'type:', typ
    print 'value:', value
    print '-----'


def exc_handler_ret():
    """An exception handler that returns something other than None."""
    return 'DIV_BY_ZERO'

# Email sending is not tested since it is impossible to send email on Travis
# server.
@exception_notifier.mail_exception(callback=exc_handler)
def f(x, y):
    return x / y


@exception_notifier.mail_exception(callback=exc_handler_ret)
def g(x, y):
    return x / y


if __name__ == '__main__':
    # Test return value of function call.
    assert f(2, 1) == 2
    # Test return value of the custom callback function.
    assert g(1, 0) == 'DIV_BY_ZERO'

    import doctest
    doctest.testmod(raise_on_error=True)
