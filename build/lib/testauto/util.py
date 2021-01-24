import logging
import os
import sys
from time import localtime, strftime
from typing import AnyStr, Tuple, List

from .case import TestCase


def gen_universal_path(src_path: str):
    """
    生成通用的路径：兼容Windows、macOS和Linux操作系统。
    :param src_path: 源路径
    :return:
    """
    if os.sep == '\\':
        return src_path.replace('/', os.sep)
    else:
        return src_path.replace('\\', os.sep)


def assert_raise(callable_obj, exception, msg=None):
    """
    断言抛出指定异常
    :param callable_obj: 可调用对象
    :param exception: 指定异常
    :param msg: 断言失败的提示信息
    :return:
    """
    if not callable(callable_obj):
        raise ValueError('入参不是可调用对象！')
    if not issubclass(exception, Exception):
        raise ValueError('入参不是Exception的子类！')
    try:
        callable_obj()
    except Exception as e:
        if isinstance(e, exception):
            return
        else:
            raise AssertionError(msg) if msg else AssertionError()
    raise AssertionError(msg) if msg else AssertionError()


def assert_not_raise(callable_obj, exception, msg=None):
    """
    断言不抛出指定异常
    :param callable_obj: 可调用对象
    :param exception: 指定异常
    :param msg: 断言失败的提示信息
    :return:
    """
    if not callable(callable_obj):
        raise ValueError('入参不是可调用对象！')
    if not issubclass(exception, Exception):
        raise ValueError('入参不是Exception的子类！')
    try:
        callable_obj()
    except Exception as e:
        if isinstance(e, exception):
            raise AssertionError(msg) if msg else AssertionError()


def parameterized(param_names: Tuple[str, ...], param_values: List[tuple]):
    """
    参数化测试装饰器
    :param param_names: 参数名
    :param param_values: 参数值
    :return:
    """

    def decorator(test_case):
        if issubclass(test_case, TestCase):
            setattr(test_case, '_param_names', param_names)
            setattr(test_case, '_param_values', param_values)
        return test_case

    return decorator


def format_timestamp(src_time: float, target_format='%Y-%m-%d %H:%M:%S'):
    """
    格式化时间戳
    :param src_time: 时间戳
    :param target_format: 格式
    :return:
    """
    return strftime(target_format, localtime(int(src_time)))


def seconds_to_time(seconds: int):
    """
    秒转换为时分秒
    :param seconds: 秒
    :return:
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '{:0>2}时{:0>2}分{:0>2}秒'.format(h, m, s)


class Writer:
    """
    写入类
    """

    def __init__(self, format_str='%(asctime)s[%(levelname)s]: %(message)s'):
        self.logger = logging
        self.logger.basicConfig(format=format_str)
        self.writer = sys.stderr

    def write_debug(self, msg):
        self.logger.log(logging.DEBUG, msg)

    def write_info(self, msg):
        self.logger.log(logging.INFO, msg)

    def write_warning(self, msg):
        self.logger.log(logging.WARNING, msg)

    def write_error(self, msg):
        self.logger.log(logging.ERROR, msg)

    def write_line(self, msg: AnyStr = ''):
        self.writer.write(msg)
        self.writer.write('\n')
