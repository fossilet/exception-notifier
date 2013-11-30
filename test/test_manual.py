#! /usr/bin/env python
"""
Script for manual tests.

Since nov. 28, 2013
"""

import sys
sys.path.insert(0, '..')

import exception_notifier as en


@en.mail_exception()
def f():
    1 / 0


def g():
    f()

if __name__ == '__main__':
    # test decorator
    g()

    # test enable
    en.enable()
    2 / 0
    en.disable()
