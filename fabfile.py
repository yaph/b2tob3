# -*- coding: utf-8 -*-
from fabric.api import local, lcd


def build_docs():
    local('python setup.py build_sphinx')


def docs():
    build_docs()
    local('python setup.py upload_sphinx')


def release():
    local('python setup.py sdist upload')


def git():
    local('git add . && git commit -a')
    local('git push')


def test():
    local('cp -R tests t')
    local('python b2tob3/b2tob3.py -d t')