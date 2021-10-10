from .base import Base
from .consts import CmdCOLOR


class Color(Base):
    cmd_type = CmdCOLOR.TYPE.value
    data_len = CmdCOLOR.DATA_LENGTH.value
    struct = CmdCOLOR.STRUCT.value

    def __init__(self, handler_execute=None):
        super().__init__(handler_execute)

    def _get_color_from_cmd(self, cmd: bytes) -> bytes:
        cmd_type, data_len, color = self.struct.unpack(cmd)
        return color

    def _execute(self, cmd: bytes):
        if self.handler_execute:
            self.handler_execute(self._get_color_from_cmd(cmd))
