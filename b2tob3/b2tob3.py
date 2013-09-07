#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Perform text replacements in all files in the current directory and sub
# directories to help migrate from bootstrap 2 to bootstrap 3.
#
# This script should be executed in a directory with HTML files or templates.
# Use at your on risk, try it on a copy first!
import os
import re
from optparse import OptionParser

# List of regular expression replacements tuples to be executed in order.
# Does not include all changes from:
# http://getbootstrap.com/getting-started/#migration

class_decl = r'(class\s*=\s*["\'][\w\s]*)'

regexes = [
    (re.compile(class_decl + r'\bspan(\d+)\b'), '\\1col-md-\\2'),
    (re.compile(class_decl + r'\boffset(\d+)\b'), '\\1col-md-offset-\\2'),
    (re.compile(class_decl + r'\bicon-(\w+)\b'), '\\1glyphicon glyphicon-\\2'),
    (re.compile(class_decl + r'\bhero\-unit\b'), '\\1jumbotron'),

    (re.compile(class_decl + r'\b(container|row)-fluid\b'), '\\1\\2'),
    (re.compile(class_decl + r'\bnav\-(collapse|toggle)\b'), '\\1navbar-\\2'),

    (re.compile(class_decl + r'\b(input|btn)-small\b'), '\\1\\2-sm'),
    (re.compile(class_decl + r'\b(input|btn)-large\b'), '\\1\\2-lg'),

    (re.compile(class_decl + r'\bbtn-navbar\b'), '\\1navbar-btn'),
    (re.compile(class_decl + r'\bbtn-mini\b'), '\\1btn-xs'),
    (re.compile(class_decl + r'\bthumbnail\b'), '\\1img-thumbnail'),
    (re.compile(class_decl + r'\bunstyled\b'), '\\1list-unstyled'),
    (re.compile(class_decl + r'\binline\b'), '\\1list-inline')
]


def main():
    parser = OptionParser()

    parser.add_option(
        "-d", "--directory", dest="pwd",
        help="Directory to search", metavar="DIR", default=os.curdir
    )

    parser.add_option(
        "-e", "--extension", dest="ext",
        help="Extension of files to parse", metavar="EXT", default="html"
    )

    (options, args) = parser.parse_args()

    pwd = os.path.abspath(options.pwd)

    count_subs = 0
    count_files = 0
    count_files_changed = 0

    for root, dirs, files in os.walk(pwd):
        for f in files:
            if f.endswith('.' + options.ext):
                count_files += 1
                fname = os.path.join(root, f)
                with open(fname, 'r') as curr_file:
                    content = curr_file.read()
                with open(fname, 'w') as curr_file:
                    count_file_subs = 0
                    for regex in regexes:
                        (content, count) = re.subn(regex[0], regex[1], content)
                        count_file_subs += count
                    curr_file.write(content)
                    if count_file_subs > 0:
                        count_subs += count_file_subs
                        count_files_changed += 1

    tpl = 'Replacements: % 6d\nFiles changed: % 5d\nFiles processed: %d\n'
    print(tpl % (count_subs, count_files_changed, count_files))

if __name__ == '__main__':
    main()