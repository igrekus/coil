from pyexpect import expect
from cncoilgcode import CNFile


def test_parse_empty_cnfile():
    cnc = CNFile('header_footer_only.cnc')

    expect(len(cnc._header)).to_equal(6)
    expect(len(cnc._commands)).to_equal(0)
    expect(len(cnc._footer)).to_equal(2)

