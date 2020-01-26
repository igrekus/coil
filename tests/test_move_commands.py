from pyexpect import expect

from cncode import LineToCommand
from cncode.bases import CommandType


def test_linetocommand_constructor():
    com = LineToCommand(1, 10, 10, 12000, 0, 0, 0, 0, 0)

    expect(com.command_type).to_equal(CommandType.LINE_TO)

    print(com)
    # expect(com.length).to_equal(0)
    # expect(com.disabled).to_equal((2, 3, 4, 5, 6, 9))
    # expect(com.is_move).to_equal(False)
    # expect(com.as_gcode).to_equal('N001 M501 P1 P0.001\nG04 P0.001\n')
    # expect([com[i] for i in range(10)]).to_equal([1, 'Fill', '', '', '', '', '', 1.0, 1.0, 0.0])


# def test_linetocommand_from_string():
#     com = LineToCommand.from_string('N001 M501 P1 P.002\nG04 P.002\n')
#
#     expect(com.command_type).to_equal(CommandType.FILL)
#     expect(com.length).to_equal(0)
#     expect(com.disabled).to_equal((2, 3, 4, 5, 6, 9))
#     expect(com.is_move).to_equal(False)
#     expect(com.as_gcode).to_equal('N001 M501 P1.0 P0.002\nG04 P0.002\n')
#     expect([com[i] for i in range(10)]).to_equal([1, 'Fill', '', '', '', '', '', 1.0, 2.0, 0.0])
