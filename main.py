#!/usr/bin/env python3

from konf import Konf
k = Konf('config.yaml')

from dota2info import Dota2info
address = k('address', str)
info_source = Dota2info(address)

from server import run_server
serving_port = k('serving_port', int, 80)

run_server(info_source, serving_port)
