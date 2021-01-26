# test_task.py
from testauto.runner import StopStrategy, RetryStrategy
from testauto.task import DefaultTestTask, TestCasePriorityShouldBe, OperationMethod

from testauto_test.test_case import *

# 这是冒烟测试用例对应的测试任务
test_task_001 = DefaultTestTask()
test_task_001.add_test_cases(TestCase001(), TestCase002())

# 这是回归测试用例对应的测试任务
test_task_002 = DefaultTestTask()
test_task_002.add_test_cases(TestCase001(), TestCase004())

test_task_003 = DefaultTestTask()
test_task_003.add_test_cases_by_files(
    r'E:\Software Testing\Software Development\Python\PycharmProjects\testauto\testauto_test\test_case.py')
test_task_003.add_filter(TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P0))
test_task_003.filter_test_cases()


def test_task_004():
    test_task = DefaultTestTask()
    test_task.add_test_cases(TestCase001(), TestCase002())
    return test_task


test_task_005 = DefaultTestTask()
test_task_005.add_test_cases(TestCase006(), TestCase007())

test_task_006 = DefaultTestTask()
test_task_006.add_test_cases_by_classes('testauto_test.test_case.TestCase008')

test_task_007 = DefaultTestTask()
test_task_007.add_test_cases(TestCase012(), TestCase013(), TestCase014(), TestCase015())

if __name__ == '__main__':
    # main(test_task=test_task_001)  # 执行冒烟测试
    # main(test_task=test_task_002)  # 执行回归测试
    # main(test_task=test_task_003)
    # main(test_task=test_task_005, parallel=2)
    # main(test_task=test_task_006)
    # main(stop_strategy=StopStrategy.FIRST_NOT_PASS)
    # main(stop_strategy=RetryStrategy.RERUN_NOW)
    # main(timeout=60)
    main(test_task=test_task_007)
