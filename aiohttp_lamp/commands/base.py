from abc import ABC, abstractmethod
from struct import Struct
from .consts import (
    CmdFormat,
    ValidateMsgRetval,
    ValidateCmdRetval,
    CmdRunRetval
)
from .utils import parse_header_cmd


class Base(ABC):
    def __init__(self, handler_execute=None):
        self.handler_execute = handler_execute

    @property
    @abstractmethod
    def cmd_type(self) -> bytes:
        pass

    @property
    @abstractmethod
    def data_len(self) -> int:
        pass

    @property
    @abstractmethod
    def struct(self) -> Struct:
        pass

    _parsed_cmd_type = None
    _parsed_data_len = None

    def _parse_header_cmd(self, cmd: bytes) -> None:
        self._parsed_cmd_type, self._parsed_data_len = parse_header_cmd(cmd)

    def _validate_msg(self, msg: bytes) -> ValidateMsgRetval:
        if not msg:
            return ValidateMsgRetval.EMPTY_MSG
        if not isinstance(msg, bytes):
            return ValidateMsgRetval.INVALID_TYPE_MSG
        if len(msg) < CmdFormat.HANDLER_SIZE.value:
            return ValidateMsgRetval.INVALID_MSG_LENGTH
        self._parse_header_cmd(msg)
        if len(msg) != CmdFormat.HANDLER_SIZE.value + self._parsed_data_len:
            return ValidateMsgRetval.INVALID_MSG_LENGTH
        return ValidateMsgRetval.VALID_MSG

    def _validate_cmd(self, cmd: bytes) -> ValidateCmdRetval:
        if self._parsed_cmd_type != self.cmd_type:
            return ValidateCmdRetval.UNKNOWN_CMD
        if self._parsed_data_len != self.data_len:
            return ValidateCmdRetval.INVALID_CMD_LENGTH
        return ValidateCmdRetval.VALID_CMD

    @abstractmethod
    def _execute(self, cmd: bytes):
        pass

    def run(self, cmd: bytes) -> CmdRunRetval:
        if self._validate_msg(cmd) != ValidateMsgRetval.VALID_MSG:
            return CmdRunRetval.INVALID_MSG
        if self._validate_cmd(cmd) != ValidateCmdRetval.VALID_CMD:
            return CmdRunRetval.INVALID_CMD
        self._execute(cmd)
        return CmdRunRetval.CMD_COMPLETED_SUCCESSFULLY
