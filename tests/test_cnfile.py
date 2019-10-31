import os
from pyexpect import expect
from cncoilgcode import CNFile

file = '../gcode/VCOMTEST.CNC'


def test_parse_cnfile():
    cnc = CNFile(file)

