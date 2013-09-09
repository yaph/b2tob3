# -*- coding: utf-8 -*-
from fabric.api import local


def build_docs():
    local('python setup.py build_sphinx')


def docs():
    build_docs()
    local('python setup.py upload_sphinx')


def release():
    local('nosetests')
    local('python setup.py sdist upload')


def git():
    local('nosetests')
    local('cp docs/index.rst README.rst')
    local('git add . && git commit -a')


def reinstall():
    local('pip uninstall -y b2tob3')
    local('python setup.py install')