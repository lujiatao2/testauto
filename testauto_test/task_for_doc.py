# task_for_doc.py
from testauto.runner import StopStrategy, RetryStrategy
from testauto.task import DefaultTestTask, TestCasePriorityShouldBe, OperationMethod

from testauto_test.case_for_doc import *

# 冒烟测试用例对应的测试任务
test_task_01 = DefaultTestTask()
test_task_01.add_test_cases(TestCase01(), TestCase02())

# 回归测试用例对应的测试任务
test_task_02 = DefaultTestTask()
test_task_02.add_test_cases(TestCase01(), TestCase03())

test_task_03 = DefaultTestTask()
test_task_03.add_test_cases_by_files(
    r'E:\Software_Testing\Software Development\Python\PycharmProjects\testauto\testauto_test\case_for_doc.py')
test_task_03.add_filter(TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P0))
test_task_03.filter_test_cases()


def test_task_04():
    test_task = DefaultTestTask()
    test_task.add_test_cases(TestCase01(), TestCase02())
    return test_task


test_task_05 = DefaultTestTask()
test_task_05.add_test_cases(TestCase07(), TestCase08())

test_task_06 = DefaultTestTask()
test_task_06.add_test_cases_by_classes('testauto_test.case_for_doc.TestCase09')

test_task_07 = DefaultTestTask()
test_task_07.add_test_cases(TestCase13(), TestCase14(), TestCase15(), TestCase16())

if __name__ == '__main__':
    # main(test_task=test_task_01)  # 执行冒烟测试
    # main(test_task=test_task_02)  # 执行回归测试
    # main(test_task=test_task_03)
    # main(test_task=test_task_05, parallel=2)
    # main(test_task=test_task_06)
    # main(stop_strategy=StopStrategy.FIRST_NOT_PASS)
    # main(retry_strategy=RetryStrategy.RERUN_NOW)
    # main(timeout=60)
    main(test_task=test_task_07)
