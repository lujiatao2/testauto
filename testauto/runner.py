import traceback
from abc import ABC, abstractmethod
from concurrent.futures._base import wait, FIRST_EXCEPTION
from concurrent.futures.thread import ThreadPoolExecutor
from enum import Enum
from threading import Thread, Event
from time import perf_counter, time

from .case import TestCaseResult, TestCasePriority, TestCase
from .recorder import TestRecorder
from .task import TestTask


class StopStrategy(Enum):
    ALL_COMPLETED = ('全部完成', 0)
    FIRST_NOT_PASS = ('第一个未执行成功', 1)
    FIRST_P0_NOT_PASS = ('第一个P0测试用例未执行成功', 2)


class RetryStrategy(Enum):
    NOT_RERUN = ('不重试', 0)
    RERUN_NOW = ('立即重新执行测试用例', 1)  # 对当前未执行成功的测试用例，立即重新执行一次
    RERUN_LAST = ('最后重新执行测试用例', 2)  # 对全部未执行成功的测试用例，最后批量重新执行一次


class TestCaseThread(Thread):
    """
    测试用例执行线程
    """

    def __init__(self, test_case: TestCase):
        super().__init__()
        self.test_case = test_case
        self.exception = None

    def run(self):
        try:
            self.test_case.setup()
            self.test_case.test_case()
            self.test_case.teardown()
        except Exception as e:
            self.exception = e


class TestRunner(ABC):
    """
    测试执行器抽象类
    """

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class DefaultTestRunner(TestRunner):
    """
    默认测试执行器实现类
    """

    def run(self, test_task: TestTask, test_recorder: TestRecorder, stop_strategy: StopStrategy,
            retry_strategy: RetryStrategy, timeout: int, parallel: int):
        self.test_task = test_task
        self.test_recorder = test_recorder
        self.test_recorder.test_cases = self.test_task.test_cases
        self.stop_strategy = stop_strategy
        self.retry_strategy = retry_strategy
        self.timeout = timeout
        self.parallel = parallel
        self.test_recorder.start_time = time()
        self._run_test_task()
        self.test_recorder.end_time = time()
        self.test_recorder.calculate_test_result()
        if self.test_recorder.total_count != self.test_recorder.pass_count and self.retry_strategy == RetryStrategy.RERUN_LAST:
            self._run_test_task()
            self.test_recorder.end_time = time()
            self.test_recorder.calculate_test_result()
        self.test_recorder.gen_test_report()

    def _run_test_task(self):
        """
        执行测试任务
        :return:
        """
        with ThreadPoolExecutor(max_workers=self.parallel) as executor:
            futures = list()
            stop_event = Event()
            for test_case in self.test_task.test_cases:
                if test_case.result != TestCaseResult.PASS:
                    futures.append(executor.submit(self._run_test_case, test_case, stop_event))
            wait(futures, return_when=FIRST_EXCEPTION)  # 第一次抛出异常时返回结果

    def _run_test_case(self, test_case: TestCase, stop_event: Event):
        """
        执行测试用例
        :param test_case: 测试用例
        :param stop_event: 停止事件
        :return:
        """
        if stop_event.is_set():  # 设置了停止事件，则不再执行测试用例
            return
        self.test_recorder.start_run(test_case)
        try:
            start_time = perf_counter()
            thread = TestCaseThread(test_case)
            thread.start()
            thread.join(self.timeout)
            end_time = perf_counter()
            take_time = end_time - start_time
            if take_time > self.timeout:
                raise TimeoutError
            elif thread.exception:
                raise thread.exception
            else:
                self.test_recorder.stop_run(test_case, TestCaseResult.PASS)
        except Exception as first:
            if isinstance(first, AssertionError):
                self.test_recorder.stop_run(test_case, TestCaseResult.FAIL, traceback.format_exc())
            elif isinstance(first, TimeoutError):
                self.test_recorder.stop_run(test_case, TestCaseResult.TIMEOUT, f'执行单个测试用例超时，超时时间为：{self.timeout}秒')
            else:
                self.test_recorder.stop_run(test_case, TestCaseResult.BLOCK, traceback.format_exc())
            if self.stop_strategy == StopStrategy.FIRST_NOT_PASS or self.stop_strategy == StopStrategy.FIRST_P0_NOT_PASS and test_case.priority == TestCasePriority.P0:
                self.retry_strategy = RetryStrategy.NOT_RERUN  # 终止策略优先级大于重试策略
                stop_event.set()
                raise Exception
            if self.retry_strategy == RetryStrategy.RERUN_NOW:
                try:
                    start_time = perf_counter()
                    thread = TestCaseThread(test_case)
                    thread.start()
                    thread.join(self.timeout)
                    end_time = perf_counter()
                    take_time = end_time - start_time
                    if take_time > self.timeout:
                        raise TimeoutError
                    elif thread.exception:
                        raise thread.exception
                    else:
                        self.test_recorder.stop_run(test_case, TestCaseResult.PASS)
                except Exception as second:
                    if isinstance(second, AssertionError):
                        self.test_recorder.stop_run(test_case, TestCaseResult.FAIL, traceback.format_exc())
                    elif isinstance(second, TimeoutError):
                        self.test_recorder.stop_run(test_case, TestCaseResult.TIMEOUT,
                                                    f'执行单个测试用例超时，超时时间为：{self.timeout}秒')
                    else:
                        self.test_recorder.stop_run(test_case, TestCaseResult.BLOCK, traceback.format_exc())
