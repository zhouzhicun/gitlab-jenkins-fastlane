

# -*- coding: utf-8 -*-

import os
import sys
import types
import datetime

import PackageConfig
import FileManager
import Package

def main():

    print os.environ

    print os.path.dirname(os.environ["WORKSPACE"])

main()

