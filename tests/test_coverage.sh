#!/bin/bash

# Test and show code coverage.
# mardi 3 décembre 2013, 16:41:04 (UTC+0800)

coverage run tests/test.py
coverage html
xdg-open htmlcov/index.html
