#!/bin/bash

# Test and show code coverage.
# mardi 3 décembre 2013, 16:41:04 (UTC+0800)

set -x

echo "Must run in the repo root."

coverage run tests/test.py
coverage html

if [ -x xdg-open ]; then
  xdg-open htmlcov/index.html
else
  open htmlcov/index.html
fi
