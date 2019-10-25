import os
from pyexpect import expect
from cncoilgcode import CNFile

file = '../gcode/VCOMTEST.CNC'


def test_parse_cnfile():
    with open(file, 'rt') as f:
        cnc = CNFile(f.readlines())

