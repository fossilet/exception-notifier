"""Test script.
"""

import sys
import traceback

import exception_notifier


def exc_handler():
    typ, value, tb = sys.exc_info()
    print '-----'
    print 'type:', typ
    print 'value:', value
    print 'stack traces:', traceback.extract_tb(tb)
    print '-----'


@exception_notifier.mail_exception(callback=exc_handler, both=True)
def f(x, y):
    return x / y


if __name__ == '__main__':
    assert f(2, 1) == 2
    f(1, 0)
