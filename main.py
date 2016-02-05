#!/usr/bin/env python3

from konf import Konf
k = Konf('config.yaml')

address = k('address', str)
serving_port = k('serving_port', int, 80)

from dota2info import Dota2info

d = Dota2info(address)

