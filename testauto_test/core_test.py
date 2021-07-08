from time import sleep

from testauto import main
from testauto.case import TestCase, TestCasePriority
from testauto.recorder import DefaultTestRecorder
from testauto.runner import DefaultTestRunner
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


# 测试IDE执行入口
if __name__ == '__main__':
    main(__file__)
    main(test_recorder=DefaultTestRecorder(), test_runner=DefaultTestRunner())


# 测试命令行执行入口
def test_task_func_01():
    test_task = DefaultTestTask()
    test_task.add_test_case(TestCase01())
    return test_task


def test_recorder_func():
    return DefaultTestRecorder()


def test_runner_func():
    return DefaultTestRunner()


def test_task_func_02():
    test_task = DefaultTestTask()
    test_task.add_test_cases(TestCase03(), TestCase04(), TestCase05())
    return test_task


def test_task_func_03():
    test_task = DefaultTestTask()
    test_task.add_test_cases(TestCase01(), TestCase02())
    return test_task
