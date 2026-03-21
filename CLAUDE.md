# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

Python library that emails exception notifications to developers. Works with
Python 2.7, 3.5, and PyPy.

## Common Commands

- Run tests: `coverage run tests/test.py` or
  `python -m unittest tests.test.travis_suite`
- Full coverage report: `./tests/test_coverage.sh`
- Install: `pip install exception-notifier` or `python setup.py install`

## Architecture

Single-module package: `exception_notifier.py`

**Main API:**

- `mail_exception(**config)` - Decorator that wraps a function to catch and
  email exceptions
- `enable(**config)` - Override `sys.excepthook` to catch all uncaught
  exceptions
- `disable()` - Restore default exception hook

**Configuration options:** `sender`, `receivers`, `mail_server`, `callback`,
`args`, `kwargs`, `both`

The library uses `cgitb` to generate HTML-formatted exception details and sends
email via SMTP.
