import logging
import os
from logging import LogRecord
from pathlib import Path


class PycharmFormatter(logging.Formatter):
    """
    增加在pycharm里key直接点击文件路径跳转到代码位置的功能
    """

    def format(self, record: LogRecord):
        # todo: 仍旧有部分路径无法跳转
        # Get the pathname from record and remove the absolute path part
        cwd = os.getcwd()

        # if record.pathname.startswith(sys.path[0]):
        #     relative_path = record.pathname[len(sys.path[0]) + 1:]
        # else:
        #     relative_path = record.pathname

        path = Path(record.pathname)
        if path.is_relative_to(cwd):
            relative_path = path.relative_to(cwd)
        else:
            relative_path = record.pathname

        record.relative_path = relative_path
        record.level_name = record.levelname[0]
        if not hasattr(record, 'interval'):
            record.interval = 0  # 如果没有 interval，设置为 0
        return super().format(record)
