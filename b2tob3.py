#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Perform text replacements in all files in the current directory and sub
# directories to help migrate from bootstrap 2 to bootstrap 3.
#
# This script should be executed in a directory with HTML files or templates.
# Use at your on risk, try it on a copy first!
import os
import re

# List of regular expression replacements tubles to be executed in order.
# Does not include all changes from:
# http://getbootstrap.com/getting-started/#migration
regexes = [
    (re.compile(r'\bspan([1-9]+)\b'), 'col-md-\\1'),
    (re.compile(r'\bhero\-unit\b'), 'jumbotron'),

    (re.compile(r'\b(container|row)-fluid\b'), '\\1'),
    (re.compile(r'\bnav\-(collapse|toggle)\b'), 'navbar-\\1'),

    (re.compile(r'\b(input|btn)-small\b'), '\\1-sm'),
    (re.compile(r'\b(input|btn)-large\b'), '\\1-lg'),

    (re.compile(r'\bbtn-navbar\b'), 'navbar-btn'),
    (re.compile(r'\bbtn-mini\b'), 'btn-xs'),
    (re.compile(r'\bthumbnail\b'), 'img-thumbnail'),
    (re.compile(r'\bunstyled\b'), 'list-unstyled')
]

pwd = os.path.abspath(os.curdir)
for root, dirs, files in os.walk(pwd):
    for f in files:
        fname = os.path.join(root, f)
        with open(fname, 'r') as curr_file:
            content = curr_file.read()
        with open(fname, 'w') as curr_file:
            for regex in regexes:
                content = re.sub(regex[0], regex[1], content)
            curr_file.write(content)