#! /usr/bin/env python
"""
Test if this module breaks the basic behavior of exception in Python.

It turns out that both cgitb.handler and exception_notifier.mail_exception does
not terminate the program after handling exception. This is a violation of
default Python behavior.

Since nov. 30, 2013
"""

import sys
sys.path.insert(0, '..')

import exception_notifier as en
import cgitb

cgitb.enable()


def f():
    1 / 0


if __name__ == '__main__':
    en.enable()
    f()
    en.disable()

    try:
        f()
    except:
        cgitb.handler()
    print("After an exception is caught, should this show up?")
