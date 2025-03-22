import inspect

from hogwarts_logger import Logger


def get_invoker_module_name():
    for frame in inspect.stack():
        if inspect.ismodule(frame.function):
            module_name = frame.filename.__name__
        else:
            module = inspect.getmodule(frame.function, _filename=frame.filename)
            module_name = module.__name__.partition('.')[0]
        print(module_name)


def test_logger_name():
    get_invoker_module_name()


def test_logger_name_none():
    x = Logger.get_invoker_package_name()
    assert x == '_pytest'
