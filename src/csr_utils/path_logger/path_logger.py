from __future__ import annotations
import logging
from logging import Logger
from typing import Union, Dict

from csr_utils.path_logger.pycharm_formatter import PycharmFormatter
from csr_utils.path_logger.time_interval_filter import TimeIntervalFilter


class PathLogger():
    logger_dict: Dict[str, PathLogger] = {}

    def __init__(self, name=None):
        self.logger = None
        self.name = name
        self.last = None

    def init_logger(self, name):
        """
        延迟初始化logger，避免影响其他的logger
        """
        path_logger = logging.getLogger(name=name)
        path_logger.setLevel(logging.INFO)
        formatter = PycharmFormatter(
            '%(relative_path)s:%(lineno)s %(asctime)s %(interval).2fs %(level_name)01s %(message)s'
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

    def log(self, msg, level=logging.NOTSET, *args, **kwargs):
        self._get_logger().log(level, msg, stacklevel=2, *args, **kwargs)

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
        if isinstance(level, int):
            if level == 1:
                level = logging.DEBUG
            elif level == 2:
                level = logging.NOTSET
            else:
                ...
        elif isinstance(level, str):
            level = level.upper()

        self._get_logger().setLevel(level)
        self._get_logger().debug(f'log level =  {logging.getLevelName(level)}')

        # 控制台的输出，pytest是可以控制的, logger的handler的level默认是NOSET

        # for handle in self.logger.handlers:
        #     handle.setLevel(level)

    def get_log_actions(self):
        return [
            self.log,
            self.debug,
            self.info,
            self.warn,
            self.error,
            self.critical,
        ]
