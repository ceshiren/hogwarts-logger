import inspect
import logging
import os
from logging import LogRecord
from pathlib import Path


class PycharmFormatter(logging.Formatter):
    """
    增加在pycharm里key直接点击文件路径跳转到代码位置的功能
    """

    def get_invoke(self, record: LogRecord):
        # 获取当前堆栈信息
        stack = inspect.stack()
        for i, s in enumerate(stack):
            if s.filename.rpartition(os.sep)[-1] == record.filename and s.lineno == record.lineno:
                # 被调用方
                index = i + 1
                break
        else:
            index = None

        # 检查是否有父级调用函数

        if index:
            invoke = f'{stack[index].function}:{record.funcName}'  # 获取父级调用函数名
        else:
            invoke = f'{record.funcName}'
        return invoke

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

        if record.levelno <= logging.DEBUG:
            record.invoke = self.get_invoke(record)
        else:
            record.invoke = record.funcName

        record.level_name = record.levelname[0]
        if not hasattr(record, 'interval'):
            record.interval = 0  # 如果没有 interval，设置为 0
        return super().format(record)
