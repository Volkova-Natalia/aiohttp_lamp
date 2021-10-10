from .base import Base
from .consts import CmdOFF


class Off(Base):
    cmd_type = CmdOFF.TYPE.value
    data_len = CmdOFF.DATA_LENGTH.value
    struct = CmdOFF.STRUCT.value

    def __init__(self, handler_execute=None):
        super().__init__(handler_execute)

    def _execute(self, cmd: bytes):
        if self.handler_execute:
            self.handler_execute()
