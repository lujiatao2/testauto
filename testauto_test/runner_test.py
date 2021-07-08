from time import sleep

from testauto import main
from testauto.case import TestCase, TestCasePriority
from testauto.runner import StopStrategy, RetryStrategy
from testauto.task import DefaultTestTask


class TestCase01(TestCase):

    def test_case(self):
        sleep(1)


class TestCase02(TestCase):

    def test_case(self):
        sleep(2)


class TestCase03(TestCase):
    title = 'TestCase03'
    priority = TestCasePriority.P1

    def test_case(self):
        assert False


class TestCase04(TestCase):
    title = 'TestCase04'
    priority = TestCasePriority.P0

    def test_case(self):
        assert False


class TestCase05(TestCase):
    title = 'TestCase05'
    priority = TestCasePriority.P0

    def test_case(self):
        ...


if __name__ == '__main__':
    # 单线程和多线程执行测试用例
    # main()
    # main(parallel=2)

    # 不同的终止策略
    # test_task_01 = DefaultTestTask()
    # test_task_01.add_test_cases(TestCase03(), TestCase04(), TestCase05())
    # main(test_task=test_task_01, stop_strategy=StopStrategy.FIRST_NOT_PASS)
    # main(test_task=test_task_01, stop_strategy=StopStrategy.FIRST_P0_NOT_PASS)

    # 不同的重试策略
    # test_task_02 = DefaultTestTask()
    # test_task_02.add_test_cases(TestCase03(), TestCase04(), TestCase05())
    # main(test_task=test_task_02, retry_strategy=RetryStrategy.RERUN_NOW)
    # main(test_task=test_task_02, retry_strategy=RetryStrategy.RERUN_LAST)

    # 测试用例执行超时
    test_task_03 = DefaultTestTask()
    test_task_03.add_test_cases(TestCase01(), TestCase02())
    main(test_task=test_task_03, timeout=2)
