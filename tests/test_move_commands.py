from euclid3 import LineSegment2, Point2
from pyexpect import expect

from cncode import LineToCommand
from cncode.bases import CommandType


def test_linetocommand_constructor():
    com = LineToCommand(1, 10.0, 10.0, 12000, 0, None, None)

    expect(com.command_type).to_equal(CommandType.LINE_TO)
    expect([com[i] for i in range(10)]).to_equal([1, 'Line To', 10, 10, '*', '', 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.length).almost_equal(14.14, 0.01)
    expect(com.disabled).to_equal((5, 8, 9))

    gui = com.gui_geometry[-1]
    expect(gui.p1).to_equal(Point2(0, 0))
    expect(gui.p2).to_equal(Point2(10, 10))

    gcode = com.gcode_geometry[-1]
    expect(gcode.p1).to_equal(Point2(0, 0))
    expect(gcode.p2).to_equal(Point2(10, 10))

    expect(com.gcode_end_x).to_equal(10.0)
    expect(com.gcode_end_y).to_equal(10.0)

    expect(com.as_gcode).to_equal('N001 M500 P0\n     F12000\n     G01 X10.0 Y10.0 Z0\n')


def test_linetocommand_from_string():
    com = LineToCommand.from_string(string='N001 M500 P1\n     F12000\n     G01 X0 Y5 Z0\n',
                                    prev_gui_end=Point2(0, 0), prev_gcode_end=Point2(0, 0))

    expect(com.command_type).to_equal(CommandType.LINE_TO)
    expect([com[i] for i in range(10)]).to_equal([1, 'Line To', 0, 5.0, '*', '', 12000, 1.0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.length).to_equal(5)
    expect(com.disabled).to_equal((5, 8, 9))

    gui = com.gui_geometry[-1]
    expect(gui.p1).to_equal(Point2(0, 0))
    expect(gui.p2).to_equal(Point2(0, 5))

    gcode = com.gcode_geometry[-1]
    expect(gcode.p1).to_equal(Point2(0, 0))
    expect(gcode.p2).to_equal(Point2(0, 5))

    expect(com.gcode_end_x).to_equal(0)
    expect(com.gcode_end_y).to_equal(5)

    expect(com.as_gcode).to_equal('N001 M500 P1.0\n     F12000\n     G01 X0.0 Y5.0 Z0\n')
