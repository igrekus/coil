from pyexpect import expect

from cncode import FillCommand, WeldCommand, SonoUpCommand


def test_fillcommand_constructor():
    fill = FillCommand(1, 1, 1)

    expect(fill.length).to_equal(0)
    expect(fill.disabled).to_equal((2, 3, 4, 5, 6, 9))
    expect(fill.is_move).to_equal(False)
    expect(fill.as_gcode).to_equal('N001 M501 P1 P0.001\nG04 P0.001\n')
    expect([fill[i] for i in range(10)]).to_equal([1, 'Fill', '', '', '', '', '', 1.0, 1.0, 0.0])


def test_fillcommand_from_string():
    fill = FillCommand.from_string('N001 M501 P1 P.002\nG04 P.002\n')

    expect(fill.length).to_equal(0)
    expect(fill.disabled).to_equal((2, 3, 4, 5, 6, 9))
    expect(fill.is_move).to_equal(False)
    expect(fill.as_gcode).to_equal('N001 M501 P1.0 P0.002\nG04 P0.002\n')
    expect([fill[i] for i in range(10)]).to_equal([1, 'Fill', '', '', '', '', '', 1.0, 2.0, 0.0])


def test_weldcommand_constructor():
    weld = WeldCommand(1, 1.1)

    expect(weld.length).to_equal(0)
    expect(weld.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(weld.is_move).to_equal(False)
    expect(weld.as_gcode).to_equal('N001 M70 P1 P0\n')
    expect([weld[i] for i in range(10)]).to_equal([1, 'Weld', '', '', '', '', '', '', '', 1.1])


def test_weldcommand_from_string():
    weld = WeldCommand.from_string('N003 M70 P20 P0\n')

    expect(weld.length).to_equal(0)
    expect(weld.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(weld.is_move).to_equal(False)
    expect(weld.as_gcode).to_equal('N003 M70 P20 P0\n')
    expect([weld[i] for i in range(10)]).to_equal([3, 'Weld', '', '', '', '', '', '', '', 20.0])


def test_sonoupcommand_constructor():
    sonoup = SonoUpCommand(1, 1.1)

    expect(sonoup.length).to_equal(0)
    expect(sonoup.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(sonoup.is_move).to_equal(False)
    expect(sonoup.as_gcode).to_equal('N001 M71 P1 P0\n')
    expect([sonoup[i] for i in range(10)]).to_equal([1, 'Sono Up', '', '', '', '', '', '', '', 1.1])


def test_sonoupcommand_from_string():
    sonoup = SonoUpCommand.from_string('N004 M71 P20 P0\n')

    expect(sonoup.length).to_equal(0)
    expect(sonoup.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(sonoup.is_move).to_equal(False)
    expect(sonoup.as_gcode).to_equal('N004 M71 P20 P0\n')
    expect([sonoup[i] for i in range(10)]).to_equal([4, 'Sono Up', '', '', '', '', '', '', '', 20.0])
