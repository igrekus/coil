from euclid3 import Point2
from pyexpect import expect

from cncode import LineToCommand, CwShortArcToCommand, CcwShortArcToCommand, CwLongArcToCommand, CcwLongArcToCommand
from cncode.bases import CommandType
from cncode.move_commands import Arc, LineToWithEndCurveCommand


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


def test_cwarcshortcommand_constructor():
    com = CwShortArcToCommand(1, 5.0, 3.0, 4.0, 12000, 0.0, Point2(0, 0), Point2(0, 0))

    expect(com.command_type).to_equal(CommandType.CW_ARC_TO_SHORT)
    expect([com[i] for i in range(10)]).to_equal([1, 'CW Arc To', 5.0, 3.0, 4.0, 0, 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.disabled).to_equal((8, 9))

    gui = com.gui_geometry[-1]
    expect(len(com.gui_geometry)).to_equal(1)
    expect(gui.p1).to_equal(Point2(0, 0))
    expect(gui.p2).to_equal(Point2(5.0, 3.0))
    expect(type(gui)).to_be(Arc)
    expect(gui.c.x).almost_equal(3.909, 0.01)
    expect(gui.c.y).almost_equal(-0.84, 0.01)
    expect(gui.r).almost_equal(4, 0.01)

    expect(com.length).almost_equal(6.53, 0.01)

    expect(com.gcode_end_x).to_equal(5.0)
    expect(com.gcode_end_y).to_equal(3.0)

    expect(com.as_gcode).to_equal('N001 M500 P0.0\n     F12000\n     G02 X5.000 Y3.000 Z0 I3.909 J-0.848 K0\n')


def test_cwarcshortcommand_from_string():
    com = CwShortArcToCommand.from_string(string='N001 M500 P0\n     F12000 \n     G02 X-2 Y2 Z0 I.8708286934 J2.8708286934 K0',
                                          prev_gui_end=Point2(0, 0), prev_gcode_end=Point2(0, 0))

    expect(com.command_type).to_equal(CommandType.CW_ARC_TO_SHORT)
    expect([com[i] for i in range(10)]).to_equal([1, 'CW Arc To', -2.0, 2.0, 3.0, 0, 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.disabled).to_equal((8, 9))

    gui = com.gui_geometry[-1]
    expect(len(com.gui_geometry)).to_equal(1)
    expect(gui.p1).to_equal(Point2(0, 0))
    expect(gui.p2).to_equal(Point2(-2.0, 2.0))
    expect(type(gui)).to_be(Arc)
    expect(gui.c.x).almost_equal(0.871, 0.01)
    expect(gui.c.y).almost_equal(2.871, 0.01)
    expect(gui.r).almost_equal(3, 0.01)

    expect(com.length).almost_equal(2.95, 0.01)

    expect(com.gcode_end_x).to_equal(-2.0)
    expect(com.gcode_end_y).to_equal(2.0)

    expect(com.as_gcode).to_equal('N001 M500 P0.0\n     F12000\n     G02 X-2.000 Y2.000 Z0 I0.871 J2.871 K0\n')


def test_ccwarcshortcommand_constructor():
    com = CcwShortArcToCommand(1, 5.0, 3.0, 4.0, 12000, 0.0, Point2(0, 0), Point2(0, 0))

    expect(com.command_type).to_equal(CommandType.CCW_ARC_TO_SHORT)
    expect([com[i] for i in range(10)]).to_equal([1, 'CCW Arc To', 5.0, 3.0, 4.0, 0, 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.disabled).to_equal((8, 9))

    gui = com.gui_geometry[-1]
    expect(len(com.gui_geometry)).to_equal(1)
    expect(gui.p1).to_equal(Point2(0, 0))
    expect(gui.p2).to_equal(Point2(5.0, 3.0))
    expect(type(gui)).to_be(Arc)
    expect(gui.c.x).almost_equal(1.091, 0.01)
    expect(gui.c.y).almost_equal(3.848, 0.01)
    expect(gui.r).almost_equal(4, 0.01)

    expect(com.length).almost_equal(6.53, 0.01)

    expect(com.gcode_end_x).to_equal(5.0)
    expect(com.gcode_end_y).to_equal(3.0)

    expect(com.as_gcode).to_equal('N001 M500 P0.0\n     F12000\n     G03 X5.000 Y3.000 Z0 I1.091 J3.848 K0\n')


def test_ccwarcshortcommand_from_string():
    com = CcwShortArcToCommand.from_string(string='N001 M500 P0\n     F12000 \n     G03 X-2 Y2 Z0 I-2.8708286934 J-.8708286934 K0\n',
                                           prev_gui_end=Point2(0, 0), prev_gcode_end=Point2(0, 0))

    expect(com.command_type).to_equal(CommandType.CCW_ARC_TO_SHORT)
    expect([com[i] for i in range(10)]).to_equal([1, 'CCW Arc To', -2.0, 2.0, 3.0, 0, 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.disabled).to_equal((8, 9))

    gui = com.gui_geometry[-1]
    expect(len(com.gui_geometry)).to_equal(1)
    expect(gui.p1).to_equal(Point2(0, 0))
    expect(gui.p2).to_equal(Point2(-2.0, 2.0))
    expect(type(gui)).to_be(Arc)
    expect(gui.c.x).almost_equal(-2.871, 0.01)
    expect(gui.c.y).almost_equal(-0.871, 0.01)
    expect(gui.r).almost_equal(3, 0.01)

    expect(com.length).almost_equal(2.95, 0.01)

    expect(com.gcode_end_x).to_equal(-2.0)
    expect(com.gcode_end_y).to_equal(2.0)

    expect(com.as_gcode).to_equal('N001 M500 P0.0\n     F12000\n     G03 X-2.000 Y2.000 Z0 I-2.871 J-0.871 K0\n')


def test_cwarclongcommand_constructor():
    com = CwLongArcToCommand(1, 5.0, 3.0, 4.0, 12000, 0.0, Point2(0, 0), Point2(0, 0))

    expect(com.command_type).to_equal(CommandType.CW_ARC_TO_LONG)
    expect([com[i] for i in range(10)]).to_equal([1, 'CW Arc To', 5.0, 3.0, 4.0, 1, 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.disabled).to_equal((8, 9))

    expect(len(com.gui_geometry)).to_equal(2)
    arc1, arc2 = com.gui_geometry
    expect(arc1.c.x).almost_equal(1.091, 0.01)
    expect(arc1.c.y).almost_equal(3.848, 0.01)
    expect(arc1.r).almost_equal(4, 0.01)
    expect(arc1.p1.x).to_equal(0.0)
    expect(arc1.p1.y).to_equal(0.0)
    expect(arc1.p2.x).almost_equal(-0.966, 0.01)
    expect(arc1.p2.y).almost_equal(7.278, 0.01)

    expect(arc2.c.x).almost_equal(1.091, 0.01)
    expect(arc2.c.y).almost_equal(3.848, 0.01)
    expect(arc2.r).almost_equal(4, 0.01)
    expect(arc2.p1.x).almost_equal(-0.966, 0.01)
    expect(arc2.p1.y).almost_equal(7.278, 0.01)
    expect(arc2.p2.x).almost_equal(5.0, 0.01)
    expect(arc2.p2.y).almost_equal(3.0, 0.01)

    expect(com.length).almost_equal(18.60, 0.01)

    expect(com.gcode_end_x).to_equal(5.0)
    expect(com.gcode_end_y).to_equal(3.0)

    expect(com.as_gcode).to_equal('N001 M500 P0.0\n     F12000\n     G02 X-0.967 Y7.278 Z0 I1.091 J3.848 K0\n     G02 X5.000 Y3.000 Z0 I1.091 J3.848 K0\n')


def test_cwarclongcommand_from_string():
    # 5, 2, 3
    com = CwLongArcToCommand.from_string(string='N001 M500 P0\n     F12000\n     G02 X.8945242865 Y5.0136892838 Z0 I2.0086963156 J2.2282592111 K0\n     G02 X5 Y2 Z0 I2.0086963156 J2.2282592111 K0\n',
                                         prev_gui_end=Point2(0, 0), prev_gcode_end=Point2(0, 0))

    expect(com.command_type).to_equal(CommandType.CW_ARC_TO_LONG)
    expect([com[i] for i in range(10)]).to_equal([1, 'CW Arc To', 5.0, 2.0, 3.0, 1, 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.disabled).to_equal((8, 9))

    expect(len(com.gui_geometry)).to_equal(2)
    arc1, arc2 = com.gui_geometry
    expect(arc1.c.x).almost_equal(2.009, 0.01)
    expect(arc1.c.y).almost_equal(2.228, 0.01)
    expect(arc1.r).almost_equal(3, 0.01)
    expect(arc1.p1.x).to_equal(0.0)
    expect(arc1.p1.y).to_equal(0.0)
    expect(arc1.p2.x).almost_equal(0.894, 0.01)
    expect(arc1.p2.y).almost_equal(5.013, 0.01)

    expect(arc2.c.x).almost_equal(2.009, 0.01)
    expect(arc2.c.y).almost_equal(2.228, 0.01)
    expect(arc2.r).almost_equal(3, 0.01)
    expect(arc2.p1.x).almost_equal(0.894, 0.01)
    expect(arc2.p1.y).almost_equal(5.013, 0.01)
    expect(arc2.p2.x).almost_equal(5.0, 0.01)
    expect(arc2.p2.y).almost_equal(2.0, 0.01)

    expect(com.length).almost_equal(12.16, 0.01)

    expect(com.gcode_end_x).to_equal(5.0)
    expect(com.gcode_end_y).to_equal(2.0)

    expect(com.as_gcode).to_equal('N001 M500 P0.0\n     F12000\n     G02 X0.895 Y5.014 Z0 I2.009 J2.228 K0\n     G02 X5.000 Y2.000 Z0 I2.009 J2.228 K0\n')


def test_ccwarclongcommand_constructor():
    com = CcwLongArcToCommand(1, 5.0, 3.0, 4.0, 12000, 0.0, Point2(0, 0), Point2(0, 0))

    expect(com.command_type).to_equal(CommandType.CW_ARC_TO_LONG)
    expect([com[i] for i in range(10)]).to_equal([1, 'CCW Arc To', 5.0, 3.0, 4.0, 1, 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.disabled).to_equal((8, 9))

    expect(len(com.gui_geometry)).to_equal(2)
    arc1, arc2 = com.gui_geometry
    expect(arc1.c.x).almost_equal(3.909, 0.01)
    expect(arc1.c.y).almost_equal(-0.848, 0.01)
    expect(arc1.r).almost_equal(4, 0.01)
    expect(arc1.p1.x).to_equal(0.0)
    expect(arc1.p1.y).to_equal(0.0)
    expect(arc1.p2.x).almost_equal(5.967, 0.01)
    expect(arc1.p2.y).almost_equal(-4.278, 0.01)

    expect(arc2.c.x).almost_equal(3.909, 0.01)
    expect(arc2.c.y).almost_equal(-0.848, 0.01)
    expect(arc2.r).almost_equal(4, 0.01)
    expect(arc2.p1.x).almost_equal(5.967, 0.01)
    expect(arc2.p1.y).almost_equal(-4.278, 0.01)
    expect(arc2.p2.x).almost_equal(5.0, 0.01)
    expect(arc2.p2.y).almost_equal(3.0, 0.01)

    expect(com.length).almost_equal(18.60, 0.01)

    expect(com.gcode_end_x).to_equal(5.0)
    expect(com.gcode_end_y).to_equal(3.0)

    expect(com.as_gcode).to_equal('N001 M500 P0.0\n     F12000\n     G03 X5.967 Y-4.278 Z0 I3.909 J-0.848 K0\n     G03 X5.000 Y3.000 Z0 I3.909 J-0.848 K0\n')


def test_ccwarclongcommand_from_string():
    # 5, 2, 3
    com = CcwLongArcToCommand.from_string(string='N001 M500 P0\n     F12000\n     G03 X4.1054757135 Y-3.0136892838 Z0 I2.9913036844 J-.2282592111 K0\n     G03 X5 Y2 Z0 I2.9913036844 J-.2282592111 K0\n',
                                          prev_gui_end=Point2(0, 0), prev_gcode_end=Point2(0, 0))

    expect(com.command_type).to_equal(CommandType.CW_ARC_TO_LONG)
    expect([com[i] for i in range(10)]).to_equal([1, 'CCW Arc To', 5.0, 2.0, 3.0, 1, 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    expect(com.disabled).to_equal((8, 9))

    expect(len(com.gui_geometry)).to_equal(2)
    arc1, arc2 = com.gui_geometry
    expect(arc1.c.x).almost_equal(2.991, 0.01)
    expect(arc1.c.y).almost_equal(-0.228, 0.01)
    expect(arc1.r).almost_equal(3, 0.01)
    expect(arc1.p1.x).to_equal(0.0)
    expect(arc1.p1.y).to_equal(0.0)
    expect(arc1.p2.x).almost_equal(4.105, 0.01)
    expect(arc1.p2.y).almost_equal(-3.014, 0.01)

    expect(arc2.c.x).almost_equal(2.991, 0.01)
    expect(arc2.c.y).almost_equal(-0.228, 0.01)
    expect(arc2.r).almost_equal(3, 0.01)
    expect(arc2.p1.x).almost_equal(4.105, 0.01)
    expect(arc2.p1.y).almost_equal(-3.014, 0.01)
    expect(arc2.p2.x).almost_equal(5.0, 0.01)
    expect(arc2.p2.y).almost_equal(2.0, 0.01)

    expect(com.length).almost_equal(12.16, 0.01)

    expect(com.gcode_end_x).to_equal(5.0)
    expect(com.gcode_end_y).to_equal(2.0)

    expect(com.as_gcode).to_equal('N001 M500 P0.0\n     F12000\n     G03 X4.105 Y-3.014 Z0 I2.991 J-0.228 K0\n     G03 X5.000 Y2.000 Z0 I2.991 J-0.228 K0\n')


def test_linetowithendcurvecommand_constructor():
    com = LineToWithEndCurveCommand(2, 7.0, 12.0, 2, 12000, 0, Point2(0.0, 5.0), Point2(0.0, 5.0))

    expect(com.command_type).to_equal(CommandType.LINE_TO_END)
    expect([com[i] for i in range(10)]).to_equal([2, 'Line To', 7.0, 12.0, 2.0, '', 12000, 0, '', ''])
    expect(com.is_move).to_equal(True)
    # expect(com.length).almost_equal(14.14, 0.01)
    # expect(com.disabled).to_equal((5, 8, 9))

    # gui = com.gui_geometry[-1]
    # expect(gui.p1).to_equal(Point2(0, 0))
    # expect(gui.p2).to_equal(Point2(10, 10))
    #
    gcode = com.gcode_geometry[-1]
    # expect(gcode.p1).to_equal(Point2(0, 0))
    # expect(gcode.p2).to_equal(Point2(10, 10))
    #
    # expect(com.gcode_end_x).to_equal(10.0)
    # expect(com.gcode_end_y).to_equal(10.0)
    #
    # expect(com.as_gcode).to_equal('N001 M500 P0\n     F12000\n     G01 X10.0 Y10.0 Z0\n')


# def test_linetowithendcurvecommand_from_string():
#     com = LineToWithEndCurveCommand.from_string(string='N001 M500 P1\n     F12000\n     G01 X0 Y5 Z0\n',
#                                                 prev_gui_end=Point2(0, 0), prev_gcode_end=Point2(0, 0))
#
#     expect(com.command_type).to_equal(CommandType.LINE_TO)
#     expect([com[i] for i in range(10)]).to_equal([1, 'Line To', 0, 5.0, '*', '', 12000, 1.0, '', ''])
#     expect(com.is_move).to_equal(True)
#     expect(com.length).to_equal(5)
#     expect(com.disabled).to_equal((5, 8, 9))
#
#     gui = com.gui_geometry[-1]
#     expect(gui.p1).to_equal(Point2(0, 0))
#     expect(gui.p2).to_equal(Point2(0, 5))
#
#     gcode = com.gcode_geometry[-1]
#     expect(gcode.p1).to_equal(Point2(0, 0))
#     expect(gcode.p2).to_equal(Point2(0, 5))
#
#     expect(com.gcode_end_x).to_equal(0)
#     expect(com.gcode_end_y).to_equal(5)
#
#     expect(com.as_gcode).to_equal('N001 M500 P1.0\n     F12000\n     G01 X0.0 Y5.0 Z0\n')
