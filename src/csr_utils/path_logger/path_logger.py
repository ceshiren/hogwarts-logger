from __future__ import annotations
import logging
import threading
from logging import Logger
from time import time
from typing import Union, Dict, Optional

from csr_utils.path_logger.pycharm_formatter import PycharmFormatter
from csr_utils.path_logger.time_interval_filter import TimeIntervalFilter


class PathLogger():
    logger_dict: Dict[str, PathLogger] = {}

    def __init__(self, name=None):
        self.logger: Optional[Logger] = None
        self.name = name
        self.last = None

        self._debug_level = logging.DEBUG
        # self._verbose_level = 9
        self._trace_level = 8
        self.log_level_name: Optional[str] = None
        self.log_level: Optional[int] = None

    def init_logger(self, name=None):
        """
        延迟初始化logger，避免影响其他的logger

        如果默认，会按照线程号与时间戳生成日志
        如果name='' 生成根logger
        """

        if name is None:
            name = str(threading.current_thread().ident) + str(time())
        path_logger = logging.getLogger(name=name)
        path_logger.setLevel(logging.INFO)
        formatter = PycharmFormatter(
            '%(relative_path)s:%(lineno)s %(asctime)s %(interval).2f %(level_name)01s %(message)s'
        )

        time_interval_filter = TimeIntervalFilter()
        path_logger.addFilter(time_interval_filter)

        handler = logging.StreamHandler()
        path_logger.addHandler(handler)
        for handle in path_logger.handlers:
            handle.setFormatter(formatter)
            # handle.addFilter(time_interval_filter)

        self.logger = path_logger

    @classmethod
    def get_instance(cls, name=None):
        if cls.logger_dict.get(name) is None:
            cls.logger_dict[name] = PathLogger(name)
        return cls.logger_dict[name]

    def _get_logger(self) -> logging.Logger:
        if not self.logger:
            self.init_logger(name=self.name)
        return self.logger

    def log(self, msg, level=None, *args, **kwargs):
        level = level or self._trace_level
        self._get_logger().log(level=level, msg=msg, stacklevel=2, *args, **kwargs)

    def trace(self, msg, *args, **kwargs):
        self.log(msg, level=self._trace_level, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._get_logger().debug(msg, stacklevel=2, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._get_logger().info(msg, stacklevel=2, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self._get_logger().warning(msg, stacklevel=2, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._get_logger().error(msg, stacklevel=2, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._get_logger().critical(msg, stacklevel=2, *args, **kwargs)

    def set_level(self, level: Union[int, str]):
        """
        1 = debug 2=trace 3=notset
        """

        if isinstance(level, int):
            self.log_level = (logging.INFO - level * 10) or self._trace_level
        elif isinstance(level, str):
            level_name = level.lower()
            if level_name == 'debug':
                self.log_level = self._debug_level
            elif level_name == 'trace':
                self.log_level = self._trace_level
            elif level_name == 'info':
                self.log_level = logging.INFO
            else:
                ...

        self._get_logger().setLevel(self.log_level)

        # 控制台的输出，pytest是可以控制的, logger的handler的level默认是NOSET

        # for handle in self.logger.handlers:
        #     handle.setLevel(level)

    def get_level(self):
        return self._get_logger().getEffectiveLevel()

    def get_log_actions(self):
        return [
            self.log,
            self.debug,
            self.info,
            self.warn,
            self.error,
            self.critical,
        ]
