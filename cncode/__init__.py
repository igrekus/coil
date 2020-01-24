from cncode.static_commands import FillCommand, WeldCommand, SonoUpCommand, SonoMidCommand, SonoLowCommand, \
    CutWireCommand, EmbedOnCommand, EmbedOffCommand, PullWireCommand, HoldModuleCommand, ReleaseModuleCommand, \
    BrakeOnCommand, BrakeOffCommand, ThermodeMidCommand, ThermodeUpCommand
from cncode.move_commands import LineToCommand


def make_command(text, previous):
    lines = text.split('\n')
    length = len(lines)
    if length == 1:
        line = lines[0]
        if 'M70' in line:
            return WeldCommand(text=text, previous=previous)
        elif 'M71' in line:
            return SonoUpCommand(text=text, previous=previous)
        elif 'M72' in line:
            return SonoMidCommand(text=text, previous=previous)
        elif 'M73' in line:
            return SonoLowCommand(text=text, previous=previous)
        elif 'M74' in line:
            return CutWireCommand(text=text, previous=previous)
        elif 'M75' in line:
            return EmbedOnCommand(text=text, previous=previous)
        elif 'M76' in line:
            return EmbedOffCommand(text=text, previous=previous)
        elif 'M77' in line:
            return PullWireCommand(text=text, previous=previous)
        elif 'M78' in line:
            return HoldModuleCommand(text=text, previous=previous)
        elif 'M79' in line:
            return ReleaseModuleCommand(text=text, previous=previous)
        elif 'M80' in line:
            return BrakeOnCommand(text=text, previous=previous)
        elif 'M81' in line:
            return BrakeOffCommand(text=text, previous=previous)
        elif 'M82' in line:
            return ThermodeMidCommand(text=text, previous=previous)
        elif 'M83' in line:
            return ThermodeUpCommand(text=text, previous=previous)
    elif length == 2:
        return FillCommand(text=text, previous=previous)
    elif length == 3:
        line1, line2, line3 = lines
        if 'G01' in line3:
            return LineToCommand(text=text, previous=previous)
        elif 'G02' in line3:
            return ArcToCommand(text=text, previous=previous, arc_type=ArcType.SHORT, arc_dir=ArcDirection.CW)
        elif 'G03' in line3:
            return ArcToCommand(text=text, previous=previous, arc_type=ArcType.SHORT, arc_dir=ArcDirection.CCW)
    elif length == 4:
        # long arc = arc + arc
        *_, line3, line4 = lines
        if 'G01' not in line3 and 'G01' not in line4:
            if 'G02' in line3 and 'G02' in line4:
                return ArcToCommand(text=text, previous=previous, arc_type=ArcType.LONG, arc_dir=ArcDirection.CW)
            elif 'G03' in line3 and 'G03' in line4:
                return ArcToCommand(text=text, previous=previous, arc_type=ArcType.LONG, arc_dir=ArcDirection.CCW)
        # line + end arc
        elif 'G01' in line3 and 'G01' not in line4:
            return LineToWithEndCurveCommand(text=text, previous=previous)
        # start arc + line
        elif 'G01' not in line3 and 'G01' in line4:
            return LineToWithStartCurveCommand(text=text, previous=previous)
    elif length == 5:
        return LineToWithBothCurvesCommand(text=text, previous=previous)
    else:
        return Command(text=text, previous=previous)
