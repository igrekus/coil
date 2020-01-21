from pyexpect import expect

from cncode import FillCommand, WeldCommand, SonoUpCommand
from cncode.bases import CommandType


def test_fillcommand_constructor():
    com = FillCommand(1, 1, 1)

    expect(com.command_type).to_equal(CommandType.FILL)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 9))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M501 P1 P0.001\nG04 P0.001\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Fill', '', '', '', '', '', 1.0, 1.0, 0.0])


def test_fillcommand_from_string():
    com = FillCommand.from_string('N001 M501 P1 P.002\nG04 P.002\n')

    expect(com.command_type).to_equal(CommandType.FILL)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 9))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M501 P1.0 P0.002\nG04 P0.002\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Fill', '', '', '', '', '', 1.0, 2.0, 0.0])


def test_weldcommand_constructor():
    com = WeldCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.WELD)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M70 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Weld', '', '', '', '', '', '', '', 1.1])


def test_weldcommand_from_string():
    com = WeldCommand.from_string('N003 M70 P20 P0\n')

    expect(com.command_type).to_equal(CommandType.WELD)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N003 M70 P20 P0\n')
    expect([com[i] for i in range(10)]).to_equal([3, 'Weld', '', '', '', '', '', '', '', 20.0])


def test_sonoupcommand_constructor():
    com = SonoUpCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.SONO_UP)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M71 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Sono Up', '', '', '', '', '', '', '', 1.1])


def test_sonoupcommand_from_string():
    com = SonoUpCommand.from_string('N004 M71 P20 P0\n')

    expect(com.command_type).to_equal(CommandType.SONO_UP)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N004 M71 P20 P0\n')
    expect([com[i] for i in range(10)]).to_equal([4, 'Sono Up', '', '', '', '', '', '', '', 20.0])
