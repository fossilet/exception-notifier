# exception-notifier

Notify uncaught exceptions in your Python code.

Working with Python 2.7.

## Installation

Exception Notifier is available at
[PYPI](https://pypi.python.org/pypi/exception-notifier),
you can install it using `pip`:

    pip install exception-notifier

Or you can clone the repo and run:

    python setup.py install

## Usage

Use the `mail_exception` function to return an decorator for your function.
Then every uncaught exception in your function will be mailed to you.

        from exception_notifier import mail_exception
        
        exception_notifier_conf = {
            'sender': 'tux@localhost',
            'receivers': ['tux@localhost'],
            'mail_server': 'localhost',
        }
        
        @mail_exception(**exception_notifier_conf)
        def fancy_function():
            ...

You may better wrap your whole module in a starting script. Thus not only
functions, but every line in your moudle will be protected by
excetpion-notifier. Your module `fancy_module` may look like this:

        def func1():
            ...
        def func2():
            ...
        def main():
            func1()
            func2()

Your wrapper scripts may look like this:

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

This way you will be notified if any line in your module raises an uncaught
exception.
