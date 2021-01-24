import sys
from argparse import ArgumentParser
from importlib import import_module
from typing import Any

from .recorder import TestRecorder, DefaultTestRecorder
from .runner import TestRunner, DefaultTestRunner, StopStrategy, RetryStrategy
from .task import TestTask, DefaultTestTask


class TestAuto:

    def __init__(self, *args, **kwargs):
        """
        :param args: 测试模块，str类型
        :param kwargs: 测试参数
            test_task: 测试任务TestTask对象
            test_recorder: 测试记录器TestRecorder对象
            test_runner: 测试执行器TestRunner对象
            stop_strategy: 终止策略StopStrategy对象
            retry_strategy: 重试策略RetryStrategy对象
            timeout: 执行单个测试用例的超时时间，int类型，单位秒
            parallel: 并行执行数量，int类型
        """
        # 初始化测试任务
        if len(args) != 0:  # 通过传入的测试模块创建测试任务
            test_task: TestTask = DefaultTestTask()
            try:
                test_task.add_test_cases_by_files(*args)
            except AttributeError:
                raise ValueError('测试模块不是字符串！')
        else:
            result = kwargs.get('test_task', None)
            if result is not None:  # 通过传入的测试任务创建测试任务
                if isinstance(result, TestTask):
                    test_task = result
                else:
                    raise ValueError('test_task不是TestTask类型的对象！')
            else:  # 自动创建测试任务
                test_task: TestTask = DefaultTestTask()
                test_task.add_test_cases_by_modules('__main__')
        if len(test_task.test_cases) == 0:
            raise ValueError('没有待执行的测试用例！')
        # 初始化测试记录器
        result = kwargs.get('test_recorder', None)
        if result is not None:
            if isinstance(result, TestRecorder):
                test_recorder = result
            else:
                raise ValueError('test_recorder不是TestRecorder类型的对象！')
        else:
            test_recorder: TestRecorder = DefaultTestRecorder()
        # 初始化测试执行器
        result = kwargs.get('test_runner', None)
        if result is not None:
            if isinstance(result, TestRunner):
                test_runner = result
            else:
                raise ValueError('test_recorder不是TestRunner类型的对象！')
        else:
            test_runner: TestRunner = DefaultTestRunner()
        # 初始化终止策略
        result = kwargs.get('stop_strategy', None)
        if result is not None:
            if isinstance(result, StopStrategy):
                stop_strategy = result
            else:
                raise ValueError('stop_strategy不是StopStrategy类型的对象！')
        else:
            stop_strategy = StopStrategy.ALL_COMPLETED
        # 初始化重试策略
        result = kwargs.get('retry_strategy', None)
        if result is not None:
            if isinstance(result, RetryStrategy):
                retry_strategy = result
            else:
                raise ValueError('retry_strategy不是RetryStrategy类型的对象！')
        else:
            retry_strategy = RetryStrategy.NOT_RERUN
        # 初始化超时时间
        result = kwargs.get('timeout', None)
        if result is not None:
            if isinstance(result, int) and result > 0:
                timeout = result
            else:
                raise ValueError('timeout不是正整数！')
        else:
            timeout = 60 * 60  # 默认60分钟测试用例执行超时
        # 初始化并行执行数量
        result = kwargs.get('parallel', None)
        if result is not None:
            if isinstance(result, int) and result > 0:
                parallel = result
            else:
                raise ValueError('parallel不是正整数！')
        else:
            parallel = 1  # 默认单线程（串行）执行测试用例
        test_runner.run(test_task=test_task, test_recorder=test_recorder, stop_strategy=stop_strategy,
                        retry_strategy=retry_strategy, timeout=timeout, parallel=parallel)


class CommandLine:

    def __init__(self):
        self.test_modules = []
        self.test_task = self.test_recorder = self.test_runner = None
        self.stop_strategy = StopStrategy.ALL_COMPLETED
        self.retry_strategy = RetryStrategy.NOT_RERUN
        self.timeout = None
        self.parallel = None
        self._parse_argv()
        TestAuto(*self.test_modules, test_task=self.test_task, test_recorder=self.test_recorder,
                 test_runner=self.test_runner, stop_strategy=self.stop_strategy, retry_strategy=self.retry_strategy,
                 timeout=self.timeout, parallel=self.parallel)

    def _parse_argv(self):
        """
        解析命令行参数
        :return:
        """
        parser = ArgumentParser(prog='testauto', add_help=False)  # 禁用默认的帮助信息
        parser.add_argument('-h', '--help', action='help', help='显示帮助信息。')
        parser.add_argument('-m', '--test-modules', type=str, nargs='*',
                            help='测试模块。示例：-m E:\\path\\to\\dictionary\\module.py')
        parser.add_argument('-t', '--test-task',
                            help='测试任务。示例：-t path.to.module.callable，其中callable为返回TestTask对象的可调用对象。')
        parser.add_argument('-r', '--test-recorder',
                            help='测试记录器。示例：-r path.to.module.callable，其中callable为返回TestRecorder对象的可调用对象。')
        parser.add_argument('-rn', '--test-runner',
                            help='测试执行器。示例：-rn path.to.module.callable，其中callable为返回TestRunner对象的可调用对象。')
        parser.add_argument('-s', '--stop-strategy', type=int, help='终止策略。参数取值：0-全部完成（默认）/1-第一个未执行成功/2-第一个P0未执行成功')
        parser.add_argument('-rt', '--retry-strategy', type=int, help='重试策略。参数取值：0-不重试（默认）/1-立即重新执行测试用例/2-最后重新执行测试用例')
        parser.add_argument('-to', '--timeout', type=int, help='超时时间（单位秒）。参数取值：正整数')
        parser.add_argument('-p', '--parallel', type=int, help='并行执行数量。参数取值：正整数')
        args = parser.parse_args(sys.argv[1:])  # 接收命令行参数（排除第一个参数）
        self.test_modules = args.test_modules if args.test_modules else []
        if not self.test_modules:
            self.test_task = self._parse_object(args.test_task, TestTask) if args.test_task else None
        self.test_recorder = self._parse_object(args.test_recorder, TestRecorder) if args.test_recorder else None
        self.test_runner = self._parse_object(args.test_runner, TestRunner) if args.test_runner else None
        tmp_stop_strategy = args.stop_strategy
        stop_strategy_flag = True
        if tmp_stop_strategy:
            for stop_strategy in StopStrategy:
                if tmp_stop_strategy == stop_strategy.value[1]:
                    stop_strategy_flag = False
                    self.stop_strategy = stop_strategy
                    break
            if stop_strategy_flag:
                raise ValueError('终止策略（-s/--stop-strategy）的参数输入错误，请执行-h/-help获取帮助信息！')
        tmp_retry_strategy = args.retry_strategy
        retry_strategy_flag = True
        if tmp_retry_strategy:
            for retry_strategy in RetryStrategy:
                if tmp_retry_strategy == retry_strategy.value[1]:
                    retry_strategy_flag = False
                    self.retry_strategy = retry_strategy
                    break
            if retry_strategy_flag:
                raise ValueError('重试策略（-rt/--retry-strategy）的参数输入错误，请执行-h/-help获取帮助信息！')
        self.timeout = args.timeout if args.timeout else None
        self.parallel = args.parallel if args.parallel else None

    @staticmethod
    def _parse_object(callable_obj_src: str, target_class: Any):
        """
        执行字符串表示的可调用对象，返回指定类型的对象
        :param callable_obj_src: 字符串表示的可调用对象
        :param target_class: 指定类型
        :return:
        """
        tmp_module = import_module('.'.join(callable_obj_src.split('.')[:-1]))
        tmp_callable_name = callable_obj_src.split('.')[-1]
        if hasattr(tmp_module, tmp_callable_name):
            tmp_callable = getattr(tmp_module, tmp_callable_name)
            if callable(tmp_callable):
                tmp_object = tmp_callable()
            else:
                raise ValueError('{}不可调用！'.format(tmp_callable_name))
            if isinstance(tmp_object, target_class):
                return tmp_object
            else:
                """
                获取对象对应类的类名：object.__class__.__name__
                获取类的类名：class.__name__
                """
                raise ValueError('源对象类型{}与目标类型{}不一致！'.format(tmp_object.__class__.__name__, target_class.__name__))
        else:
            raise ValueError('无该可调用对象：{}！'.format(tmp_callable_name))
