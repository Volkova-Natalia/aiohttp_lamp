from .base import Base
from .consts import CmdON


class On(Base):
    cmd_type = CmdON.TYPE.value
    data_len = CmdON.DATA_LENGTH.value
    struct = CmdON.STRUCT.value

    def __init__(self, handler_execute=None):
        super().__init__(handler_execute)

    def _execute(self, cmd: bytes):
        if self.handler_execute:
            self.handler_execute()
