#! /usr/bin/env python
"""
Script for manual tests.

Since nov. 28, 2013
"""

import sys
sys.path.insert(0, '..')

import exception_notifier as en


def div(x, y):
    return x / y


def cb():
    return 'E'

g = en.mail_exception()(div)

if __name__ == '__main__':
    # test decorator
    g(1, 0)

    # test enable
    en.enable(callback=cb, both=True)
    # XXX: Cannot get return value of callback in exception hook.
    print(div(1, 0))
    en.disable()
