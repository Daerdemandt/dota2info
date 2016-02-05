#!/usr/bin/env python3

from konf import Konf
k = Konf('config.yaml')

address = k('address', str)
serving_port = k('serving_port', int, 80)

