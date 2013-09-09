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
from bs4 import BeautifulSoup

# List of regular expression replacements tuples to be executed in order.
# Does not include all changes from:
# http://getbootstrap.com/getting-started/#migration

regexes = [
    (re.compile(r'\bspan(\d+)\b'), 'col-md-\\1'),
    (re.compile(r'\boffset(\d+)\b'), 'col-md-offset-\\1'),
    (re.compile(r'\bicon-(\w+)\b'), 'glyphicon glyphicon-\\1'),
    (re.compile(r'\bhero\-unit\b'), 'jumbotron'),

    (re.compile(r'\b(container|row)-fluid\b'), '\\1'),
    (re.compile(r'\bnav\-(collapse|toggle)\b'), 'navbar-\\1'),

    (re.compile(r'\b(input|btn)-small\b'), '\\1-sm'),
    (re.compile(r'\b(input|btn)-large\b'), '\\1-lg'),

    (re.compile(r'\bbtn-navbar\b'), 'navbar-btn'),
    (re.compile(r'\bbtn-mini\b'), 'btn-xs'),
    (re.compile(r'\bthumbnail\b'), 'img-thumbnail'),
    (re.compile(r'\bunstyled\b'), 'list-unstyled'),
    (re.compile(r'\binline\b'), 'list-inline')
]

extensions = ('.html', '.htm')


def make_replacements(content):
    """Perform replacements in file content. Return changed content and the
    number of replacements made."""

    count_rep = 0
    for regex in regexes:
        (content, count) = re.subn(regex[0], regex[1], content)
        count_rep += count
    return (content, count_rep)


def replace_soup(soup):
    count_rep = 0

    for regex in regexes:
        matches = soup.find_all(class_=regex[0])
        for match in matches:
            classes = []
            for cls in match['class']:
                (cls, count) = re.subn(regex[0], regex[1], cls)
                classes.append(cls)

            match['class'] = ' '.join(classes)
            count_rep += count
    return count_rep


def main():
    parser = OptionParser()

    parser.add_option(
        "-d", "--directory", dest="pwd",
        help="Directory to search", metavar="DIR", default=os.curdir
    )

    parser.add_option(
        '-v', '--verbose', action='store_true', dest='verbose',
        help='Be verbose and print names of changed files.'
    )

    (options, args) = parser.parse_args()

    pwd = os.path.abspath(options.pwd)

    count_subs = 0
    count_files = 0
    count_files_changed = 0

    for root, dirs, files in os.walk(pwd):
        for f in files:
            if not f.endswith(extensions):
                continue

            count_files += 1
            count_file_subs = 0

            fname = os.path.join(root, f)
            with open(fname, 'r') as curr_file:
                content = curr_file.read()

            soup = BeautifulSoup(content)
            count_file_subs = replace_soup(soup)

            if count_file_subs == 0:
                continue

            with open(fname, 'w') as curr_file:
                curr_file.write(str(soup))
            if options.verbose:
                print('File changed: %s' % fname)

            count_subs += count_file_subs
            count_files_changed += 1

    tpl = 'Replacements:    %d\nFiles changed:   %d\nFiles processed: %d\n'
    print(tpl % (count_subs, count_files_changed, count_files))

if __name__ == '__main__':
    main()