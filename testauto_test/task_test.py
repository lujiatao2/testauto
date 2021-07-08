from testauto.case import TestCase, TestCasePriority

from testauto.task import DefaultTestTask, TestCasePriorityShouldBe, OperationMethod


# P0、已完成
class TestCase01(TestCase):
    priority = TestCasePriority.P0
    completed = True

    def test_case(self):
        print('TestCase01')


# P0、已完成
class TestCase02(TestCase):
    priority = TestCasePriority.P0
    completed = True

    def test_case(self):
        print('TestCase02')


# P1、已完成
class TestCase03(TestCase):
    priority = TestCasePriority.P1
    completed = True

    def test_case(self):
        print('TestCase03')


# P0、未完成
class TestCase04(TestCase):
    priority = TestCasePriority.P0
    completed = False

    def test_case(self):
        print('TestCase04')


if __name__ == '__main__':
    # 添加单个测试用例
    test_task_01 = DefaultTestTask()
    test_task_01.add_test_case(TestCase01())
    assert len(test_task_01.test_cases) == 1

    # 添加多个测试用例
    test_task_02 = DefaultTestTask()
    test_task_02.add_test_cases(TestCase01(), TestCase02())
    assert len(test_task_02.test_cases) == 2

    # 通过类名增加测试用例
    test_task_03 = DefaultTestTask()
    test_task_03.add_test_cases_by_classes('testauto_test.task_test.TestCase01', 'testauto_test.task_test.TestCase02',
                                           'testauto_test.task_test.TestCase03')
    assert len(test_task_03.test_cases) == 3

    # 删除测试用例
    test_task_04 = DefaultTestTask()
    test_case01 = TestCase01()
    test_case02 = TestCase02()
    test_case03 = TestCase03()
    test_task_04.add_test_cases(test_case01, test_case02, test_case03)
    assert len(test_task_04.test_cases) == 3
    test_task_04.remove_test_case(test_case01)
    assert len(test_task_04.test_cases) == 2
    test_task_04.remove_test_cases(test_case02, test_case03)
    assert len(test_task_04.test_cases) == 0

    # 添加单个测试用例过滤器
    test_task_05 = DefaultTestTask()
    test_task_05.add_filter(TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P0))
    assert len(test_task_05.test_case_filters) == 2

    # 添加多个测试用例过滤器
    test_task_06 = DefaultTestTask()
    test_task_06.add_filters(TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P0),
                             TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P1))
    assert len(test_task_06.test_case_filters) == 3

    # 删除测试用例过滤器
    test_task_07 = DefaultTestTask()
    filter_01 = TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P0)
    filter_02 = TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P1)
    filter_03 = TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P2)
    test_task_07.add_filters(filter_01, filter_02, filter_03)
    assert len(test_task_07.test_case_filters) == 4
    test_task_07.remove_filter(filter_01)
    assert len(test_task_07.test_case_filters) == 3
    test_task_07.remove_filters(filter_02, filter_03)
    assert len(test_task_07.test_case_filters) == 1

    # 过滤测试用例
    test_task_08 = DefaultTestTask()
    test_task_08.add_test_cases_by_modules('testauto_test.task_test')
    assert len(test_task_08.test_cases) == 4
    test_task_08.add_filter(TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P0))
    test_task_08.filter_test_cases()
    assert len(test_task_08.test_cases) == 2

    # 清空测试任务
    test_task_09 = DefaultTestTask()
    test_task_09.add_test_case(TestCase01())
    assert len(test_task_09.test_cases) == 1
    assert len(test_task_09.test_case_filters) == 1
    test_task_09.clear_test_task()
    assert len(test_task_09.test_cases) == 0
    assert len(test_task_09.test_case_filters) == 0
