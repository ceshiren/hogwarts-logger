import logging
import sys
from select import select
from time import sleep

import pytest

from csr_utils.path_log import *
from csr_utils.path_log import PathLogger


@pytest.fixture
def debug_logger():
    logger = PathLogger()
    logger.set_level('debug')
    yield logger


def test_path_log():
    debug('debug')
    info('info')
    warn('warn')

    logger1 = PathLogger()
    logger1.set_level(logging.DEBUG)
    logger2 = PathLogger(name='test')
    logger2.set_level(logging.INFO)

    logger1.debug('debug 1')
    logger1.debug('info 1')
    logger2.debug('test debug 2')
    logger2.info('test info 2')


def test_path_log_name():
    logger4 = PathLogger()
    logger4.set_level('DEBUG')
    logger4.debug('debug logger4')

    logger = PathLogger.get_instance()
    # logger.set_level('DEBUG')
    logger.debug('debug')
    logger.info('info')

    logger3 = logging.getLogger()
    logger3.setLevel(logging.DEBUG)
    logger3.debug('debug logger3')

    logger2 = PathLogger.get_instance()
    logger2.debug('debug')
    logger2.info('info')


def test_set_level():
    logger = PathLogger.get_instance()
    logger.info(f'path {sys.path}')

    logger.log('notset')
    logger.debug('debug')
    logger.info('info')
    logger.warn('warn')

    logger.set_level(1)
    logger.log('notset')
    logger.debug('debug')
    logger.info('info')
    logger.warn('warn')

    # todo: 这个不生效
    logger.set_level(2)
    logger.log('notset')
    logger.debug('debug')
    logger.info('info')
    logger.warn('warn')


def test_interval():
    logger = PathLogger.get_instance()
    logger.info('')
    logger.info('1')
    sleep(1)
    logger.debug('21')
    sleep(1)
    logger.info('22')
    logger.info('3')


def test_level():
    logger = PathLogger.get_instance('level')
    logger.info('')
    logger.log('trace')
    logger.debug('debug')
    logger.info('info')
    assert logger.get_level() == logging.INFO

    logger.set_level(1)
    logger.info('')
    logger.log('trace')
    logger.debug('debug')
    logger.info('info')
    assert logger.get_level() == logging.DEBUG

    logger.set_level(2)
    logger.info('')
    logger.log('trace')
    logger.debug('debug')
    logger.info('info')
    assert logger.get_level() < logging.DEBUG


def test_set_level():
    logger = PathLogger.get_instance('set_level')
    logger.set_level('INFO')


def test_formatter():
    logger = PathLogger()
    logger.set_level('debug')
    logger.info('1234')

    logger.debug('debug')


def test_parent(debug_logger):
    logger = debug_logger
    logger.debug('')

    def fun_a():
        logger.debug('a debug 父层调用展示')
        logger.info('a info 父层调用展示')

    def fun_b():
        logger.debug('b debug 父层调用展示')
        logger.info('b info 父层调用展示')
        fun_a()

    fun_b()
    logger.debug('父层调用展示')

    logger.info("设置为info级别，只展示一层函数")
    logger.set_level('info')
    fun_b()
    logger.info('父层调用展示')


def test_enable_raw(debug_logger):
    debug_logger.debug('debug')
    debug_logger.info('info')
    debug_logger.enable_raw_log()
    debug_logger.debug('debug')
    debug_logger.info('info')
