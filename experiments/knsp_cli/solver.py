#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kubernetes Node Sizing Problem
Usage:
  knsp solve --node <node_path> --app <app_path>
  knsp (-h | --help)
  knsp --version

"""

from docopt import docopt

def main():
    arguments = docopt(__doc__, version='Utility 20.0')
    print(arguments)
