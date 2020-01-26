from pyexpect import expect

from cncode import FillCommand, WeldCommand, SonoUpCommand, SonoMidCommand, SonoLowCommand, CutWireCommand, \
    EmbedOnCommand, EmbedOffCommand, PullWireCommand, HoldModuleCommand, ReleaseModuleCommand, BrakeOnCommand, \
    BrakeOffCommand, ThermodeMidCommand, ThermodeUpCommand
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


def test_sonomid_constructor():
    com = SonoMidCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.SONO_MID)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M72 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Sono Mid', '', '', '', '', '', '', '', 1.1])


def test_sonomidcommand_from_string():
    com = SonoMidCommand.from_string('N005 M72 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.SONO_MID)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N005 M72 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([5, 'Sono Mid', '', '', '', '', '', '', '', 1.0])


def test_sonolowcommand_constructor():
    com = SonoLowCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.SONO_LOW)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M73 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Sono Low', '', '', '', '', '', '', '', 1.1])


def test_sonolowcommand_from_string():
    com = SonoLowCommand.from_string('N006 M73 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.SONO_LOW)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N006 M73 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([6, 'Sono Low', '', '', '', '', '', '', '', 1.0])


def test_cutwirecommand_constructor():
    com = CutWireCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.CUT_WIRE)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M74 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Cut wire', '', '', '', '', '', '', '', 1.1])


def test_cutwirecommand_from_string():
    com = CutWireCommand.from_string('N007 M74 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.CUT_WIRE)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N007 M74 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([7, 'Cut wire', '', '', '', '', '', '', '', 1.0])


def test_embedoncommand_constructor():
    com = EmbedOnCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.EMBED_ON)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M75 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Embed on', '', '', '', '', '', '', '', 1.1])


def test_embedoncommand_from_string():
    com = EmbedOnCommand.from_string('N008 M75 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.EMBED_ON)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N008 M75 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([8, 'Embed on', '', '', '', '', '', '', '', 1.0])


def test_embedoffcommand_constructor():
    com = EmbedOffCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.EMBED_OFF)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M76 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Embed off', '', '', '', '', '', '', '', 1.1])


def test_embedoffcommand_from_string():
    com = EmbedOffCommand.from_string('N009 M76 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.EMBED_OFF)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N009 M76 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([9, 'Embed off', '', '', '', '', '', '', '', 1.0])


def test_pullwirecommand_constructor():
    com = PullWireCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.PULL_WIRE)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M77 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Pull wire', '', '', '', '', '', '', '', 1.1])


def test_pullwirecommand_from_string():
    com = PullWireCommand.from_string('N010 M77 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.PULL_WIRE)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N010 M77 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([10, 'Pull wire', '', '', '', '', '', '', '', 1.0])


def test_holdmodule_constructor():
    com = HoldModuleCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.HOLD_MODULE)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M78 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Hold module', '', '', '', '', '', '', '', 1.1])


def test_holdmodule_from_string():
    com = HoldModuleCommand.from_string('N011 M78 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.HOLD_MODULE)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N011 M78 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([11, 'Hold module', '', '', '', '', '', '', '', 1.0])


def test_releasemodulecommand_constructor():
    com = ReleaseModuleCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.RELEASE_MODULE)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M79 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Release module', '', '', '', '', '', '', '', 1.1])


def test_releasemodulecommand_from_string():
    com = ReleaseModuleCommand.from_string('N012 M79 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.RELEASE_MODULE)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N012 M79 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([12, 'Release module', '', '', '', '', '', '', '', 1.0])


def test_brakeoncommand_constructor():
    com = BrakeOnCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.BRAKE_ON)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M80 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Brake on', '', '', '', '', '', '', '', 1.1])


def test_brakeoncommand_from_string():
    com = BrakeOnCommand.from_string('N013 M80 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.BRAKE_ON)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N013 M80 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([13, 'Brake on', '', '', '', '', '', '', '', 1.0])


def test_brakeoffcommand_constructor():
    com = BrakeOffCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.BRAKE_OFF)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M81 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Brake off', '', '', '', '', '', '', '', 1.1])


def test_brakeoffcommand_from_string():
    com = BrakeOffCommand.from_string('N014 M81 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.BRAKE_OFF)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N014 M81 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([14, 'Brake off', '', '', '', '', '', '', '', 1.0])


def test_thermodemidcommand_constructor():
    com = ThermodeMidCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.THERM_MID)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M82 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Thermode Mid', '', '', '', '', '', '', '', 1.1])


def test_thermodemid_from_string():
    com = ThermodeMidCommand.from_string('N015 M82 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.THERM_MID)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N015 M82 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([15, 'Thermode Mid', '', '', '', '', '', '', '', 1.0])


def test_thermodeupcommand_constructor():
    com = ThermodeUpCommand(1, 1.1)

    expect(com.command_type).to_equal(CommandType.THERM_UP)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N001 M83 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([1, 'Thermode Up', '', '', '', '', '', '', '', 1.1])


def test_thermodeup_from_string():
    com = ThermodeUpCommand.from_string('N016 M83 P1 P0\n')

    expect(com.command_type).to_equal(CommandType.THERM_UP)
    expect(com.length).to_equal(0)
    expect(com.disabled).to_equal((2, 3, 4, 5, 6, 7, 8))
    expect(com.is_move).to_equal(False)
    expect(com.as_gcode).to_equal('N016 M83 P1 P0\n')
    expect([com[i] for i in range(10)]).to_equal([16, 'Thermode Up', '', '', '', '', '', '', '', 1.0])
