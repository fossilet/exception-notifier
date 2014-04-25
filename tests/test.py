"""Tests.

Should run for both Python 2 and 3.
"""

import sys
import unittest

sys.path.insert(0, '..')
import exception_notifier as en


def exc_handler_ret():
    """An exception handler that returns something other than None."""
    return 'DIV_BY_ZERO'


def div(x, y):
    return x / y


class TestMailException(unittest.TestCase):
    """ Test mail exception function.
    """
    def test_mailexc(self):
        self.assertRaises(Exception, en.mail_exception()(div)(2, 0))

    def test_mailexc_withcb(self):
        f = en.mail_exception(callback=exc_handler_ret, both=True)(div)
        self.assertRaises(Exception, f(2, 0))
        self.assertEqual(f(2, 0), 'DIV_BY_ZERO')

    def test_mailexc_onlycb(self):
        g = en.mail_exception(callback=exc_handler_ret)(div)
        self.assertRaises(Exception, g(2, 0))
        self.assertEqual(g(2, 0), 'DIV_BY_ZERO')

mail_suite = unittest.TestLoader().loadTestsFromTestCase(TestMailException)


class TestExceptionHook(unittest.TestCase):
    """ Test case for exception hook.
    """
    def setUp(self):
        en.enable()

    def test_hook(self):
        self.assertRaises(ZeroDivisionError, div, 3, 0)

    def tearDown(self):
        en.disable()


class TestExceptionHookWithCB(unittest.TestCase):
    """ Test case for exception hook with callback function and mailing.
    """
    def setUp(self):
        en.enable(callback=exc_handler_ret, both=True)

    def test_hook(self):
        self.assertRaises(ZeroDivisionError, div, 3, 0)
        # XXX: we cannot test return value of callback function here like:
        #   self.assertEqual(div(3, 0), 'DIV_BY_ZERO')
        # since Python interpreter exits after exception is handled by
        # system exception hook.

    def tearDown(self):
        en.disable()


class TestExceptionHookOnlyCB(unittest.TestCase):
    """ Test case for exception hook with only callback function.
    """
    def setUp(self):
        en.enable(callback=exc_handler_ret)

    def test_hook(self):
        self.assertRaises(ZeroDivisionError, div, 3, 0)
        # XXX: we cannot test return value of callback function. See
        # TestExceptionHookWithCB.

    def tearDown(self):
        en.disable()

# Cannot test email sending on Travis CI.
suite1 = unittest.TestLoader().loadTestsFromTestCase(TestExceptionHook)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestExceptionHookWithCB)
suite3 = unittest.TestLoader().loadTestsFromTestCase(TestExceptionHookOnlyCB)
travis_suite = unittest.TestSuite([suite1, suite2, suite3])


if __name__ == '__main__':
    unittest.main(verbosity=2)
