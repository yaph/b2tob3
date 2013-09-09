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

# HTML class="btn" class='btn' class='something btn somethingelse'
# CSS .btn .btn.something
affix = r'(["\'\s\.])'

# omitted classs: .brand .checkbox.inline .radio.inline

regexes = [
    (re.compile(affix + r'span(\d+)' + affix), '\\1col-md-\\2\\3'),
    (re.compile(affix + r'offset(\d+)' + affix), '\\1col-md-offset-\\2\\3'),
    (re.compile(affix + r'icon-(\w+)' + affix), '\\1glyphicon glyphicon-\\2\\3'),
    (re.compile(affix + r'hero-unit' + affix), '\\1jumbotron\\2'),

    (re.compile(affix + r'(container|row)-fluid' + affix), '\\1\\2\\3'),
    (re.compile(affix + r'nav-(collapse|toggle)' + affix), '\\1navbar-\\2\\3'),

    (re.compile(affix + r'(input|btn)-small' + affix), '\\1\\2-sm\\3'),
    (re.compile(affix + r'(input|btn)-large' + affix), '\\1\\2-lg\\3'),

    (re.compile(affix + r'btn-navbar' + affix), '\\1navbar-btn\\2'),
    (re.compile(affix + r'btn-mini' + affix), '\\1btn-xs\\2'),
    (re.compile(affix + r'unstyled' + affix), '\\1list-unstyled\\2'),

    (re.compile(affix + r'(visible|hidden)-phone' + affix), '\\1\\2-sm\\3'),
    (re.compile(affix + r'(visible|hidden)-tablet' + affix), '\\1\\2-md\\3'),
    (re.compile(affix + r'(visible|hidden)-desktop' + affix), '\\1\\2-lg\\3'),

    (re.compile(affix + r'input-(prepend|append)' + affix), '\\1input-group\\3'),

    # Should these regexes be more restriced because class names are more
    # likely to occurr in other places?
    (re.compile(affix + r'inline' + affix), '\\1list-inline\\2'),
    (re.compile(affix + r'add-on' + affix), '\\1input-group-addon\\2'),
    (re.compile(affix + r'thumbnail' + affix), '\\1img-thumbnail\\2'),
]

extensions = ('.html', '.htm', '.css', '.js')


def make_replacements(content):
    """Perform replacements in file content. Return changed content and the
    number of replacements made."""

    count_rep = 0
    for regex in regexes:
        (content, count) = re.subn(regex[0], regex[1], content)
        count_rep += count
    return (content, count_rep)


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

            (content, count_file_subs) = make_replacements(content)
            if count_file_subs == 0:
                continue

            with open(fname, 'w') as curr_file:
                curr_file.write(content)
            if options.verbose:
                print(('File changed: %s' % fname))

            count_subs += count_file_subs
            count_files_changed += 1

    tpl = 'Replacements:    %d\nFiles changed:   %d\nFiles processed: %d\n'
    print((tpl % (count_subs, count_files_changed, count_files)))

if __name__ == '__main__':
    main()