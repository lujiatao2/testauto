from time import time

from testauto.case import TestCase, TestCaseResult
from testauto.recorder import DefaultTestRecorder
from testauto.task import DefaultTestTask
from testauto.util import parameterized


@parameterized(
    ('target_result',),
    [
        ('PASS',),
        ('PASS',),
        ('PASS',),
        ('FAIL',),
        ('FAIL',),
        ('BLOCK',),
        ('TIMEOUT',),
        ('NOT_EXECUTED',)
    ]
)
class TestCase01(TestCase):

    def test_case(self):
        ...


if __name__ == '__main__':
    test_task = DefaultTestTask()
    test_task.add_test_cases_by_classes('testauto_test.recorder_test.TestCase01')
    test_recorder = DefaultTestRecorder()
    test_recorder.test_cases = test_task.test_cases
    test_recorder.start_time = time()
    for test_case in test_recorder.test_cases:
        test_recorder.start_run(test_case)
        target_result = test_case.get_param_value('target_result')
        if target_result == 'PASS':
            test_recorder.stop_run(test_case, TestCaseResult.PASS)
        elif target_result == 'FAIL':
            test_recorder.stop_run(test_case, TestCaseResult.FAIL, '失败详情...')
        elif target_result == 'BLOCK':
            test_recorder.stop_run(test_case, TestCaseResult.BLOCK, '阻塞详情...')
        elif target_result == 'TIMEOUT':
            test_recorder.stop_run(test_case, TestCaseResult.TIMEOUT, '超时详情...')
        elif target_result == 'NOT_EXECUTED':
            test_recorder.stop_run(test_case, TestCaseResult.NOT_EXECUTED)
    test_recorder.end_time = time()
    test_recorder.calculate_test_result()
    test_recorder.gen_test_report()
