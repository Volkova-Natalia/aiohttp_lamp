from .commands.on import On
from .commands.off import Off
from .commands.color import Color
from .commands.consts import CmdRunRetval

from enum import Enum


class StateLamp(Enum):
    ON = 1
    OFF = 2


class Lamp:
    state = StateLamp.OFF
    color = b'\x00\x00\x00'

    def __init__(self, debug=True):
        self._cmd_handlers = [
            On(self.turn_on),
            Off(self.turn_off),
            Color(self.change_color)
        ]
        self.debug = debug

    def turn_on(self) -> None:
        self.state = StateLamp.ON

    def turn_off(self) -> None:
        self.state = StateLamp.OFF

    def change_color(self, color=None) -> None:
        if color:
            self.color = color

    def print_state(self):
        if self.debug:
            print('lamp', hex(id(self)), 'state =', self.state, 'color =', self.color)

    def execute_cmd(self, cmd: bytes) -> None:
        for cmd_handler in self._cmd_handlers:
            cmd_run_result = cmd_handler.run(cmd)
            if cmd_run_result == CmdRunRetval.INVALID_MSG:
                break
            if cmd_run_result == CmdRunRetval.CMD_COMPLETED_SUCCESSFULLY:
                self.print_state()
                break
