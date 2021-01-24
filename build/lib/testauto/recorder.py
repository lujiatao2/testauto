from abc import ABC, abstractmethod
from time import time
from typing import List, Optional

from .case import TestCase, TestCaseResult
from .util import Writer, format_timestamp, seconds_to_time


class TestRecorder(ABC):
    """
    测试记录器抽象类
    """

    def __init__(self):
        self.start_time = 0.0
        self.end_time = 0.0
        self.total_count = 0
        self.pass_count = 0
        self.fail_count = 0
        self.block_count = 0
        self.timeout_count = 0
        self.not_executed_count = 0
        self.test_cases: Optional[List[TestCase]] = None

    @abstractmethod
    def start_run(self, test_case: TestCase):
        pass

    @abstractmethod
    def stop_run(self, test_case: TestCase, result: TestCaseResult, result_detail=''):
        pass

    @abstractmethod
    def calculate_test_result(self):
        """
        统计测试结果
        :return:
        """
        pass

    @abstractmethod
    def gen_test_report(self):
        """
        生成测试报告
        :return:
        """
        pass


class DefaultTestRecorder(TestRecorder):
    """
    默认测试记录器实现类
    """

    def __init__(self):
        super().__init__()
        self.writer = Writer()

    def start_run(self, test_case: TestCase):
        test_case.start_time = format_timestamp(time(), target_format='%H:%M:%S')
        test_case.result = TestCaseResult.EXECUTING

    def stop_run(self, test_case: TestCase, result: TestCaseResult, result_detail=''):
        test_case.stop_time = format_timestamp(time(), target_format='%H:%M:%S')
        test_case.result = result
        if test_case.result == TestCaseResult.FAIL:
            self.writer.write_error('“{}”执行失败：{}'.format(test_case.title, result_detail))
        elif test_case.result == TestCaseResult.TIMEOUT:
            self.writer.write_error('“{}”执行超时：{}'.format(test_case.title, result_detail))
        elif test_case.result == TestCaseResult.BLOCK:
            self.writer.write_error('“{}”执行阻塞：{}'.format(test_case.title, result_detail))
        test_case.result_detail = result_detail

    def calculate_test_result(self):
        self.total_count = len(self.test_cases)
        test_cases = list(
            filter(lambda tmp_test_case: tmp_test_case.result != TestCaseResult.NOT_EXECUTED, self.test_cases))
        self.not_executed_count = self.total_count - len(test_cases)
        for test_case in test_cases:
            if test_case.result == TestCaseResult.PASS:
                self.pass_count += 1
            elif test_case.result == TestCaseResult.FAIL:
                self.fail_count += 1
            elif test_case.result == TestCaseResult.BLOCK:
                self.block_count += 1
            elif test_case.result == TestCaseResult.TIMEOUT:
                self.timeout_count += 1

    def gen_test_report(self):
        # 生成简单测试报告
        self.writer.write_line('=' * 150)
        self.writer.write_line('执行总数：{}'.format(self.total_count))
        start_time = format_timestamp(self.start_time)
        end_time = format_timestamp(self.end_time)
        take_time = seconds_to_time(int(self.end_time - self.start_time))
        self.writer.write_line('开始时间：{}    结束时间：{}    执行耗时：{}'.format(start_time, end_time, take_time))
        self.writer.write_line('-' * 150)
        self.writer.write_line('{:<10}{:<10}{}'.format('执行结果', '数量', '百分比（%）'))
        pass_percentage = float('{:.2f}'.format(self.pass_count / self.total_count * 100.0))
        self.writer.write_line('{:<10}{:<10}{}'.format('通过', self.pass_count, pass_percentage))
        fail_percentage = float('{:.2f}'.format(self.fail_count / self.total_count * 100.0))
        self.writer.write_line('{:<10}{:<10}{}'.format('失败', self.fail_count, fail_percentage))
        block_percentage = float('{:.2f}'.format(self.block_count / self.total_count * 100.0))
        self.writer.write_line('{:<10}{:<10}{}'.format('阻塞', self.block_count, block_percentage))
        timeout_percentage = float('{:.2f}'.format(self.timeout_count / self.total_count * 100.0))
        self.writer.write_line('{:<10}{:<10}{}'.format('超时', self.timeout_count, timeout_percentage))
        not_executed_percentage = float(
            '{:.2f}'.format(100 - pass_percentage - fail_percentage - block_percentage - timeout_percentage))
        self.writer.write_line('{:<10}{:<10}{}'.format('未执行', self.not_executed_count, not_executed_percentage))
        self.writer.write_line('=' * 150)
        # 生成HTML测试报告
        project = self.test_cases[0].project  # 取第一个测试用例的工程名作为测试报告的工程名
        with open('test-report.html', 'w', encoding='UTF-8') as file:
            file.write('<!DOCTYPE html>\n')
            file.write('<html lang="en">\n')
            file.write('<head>\n')
            file.write('    <style>\n')
            file.write('\n')
            file.write('        table, caption, tr, th, td {\n')
            file.write('            border: 2px solid gray;\n')
            file.write('            border-collapse: collapse;\n')
            file.write('        }\n')
            file.write('\n')
            file.write('    </style>\n')
            file.write('    <meta charset="UTF-8">\n')
            file.write('    <title>{}测试报告</title>\n'.format(project))
            file.write('</head>\n')
            file.write('<body>\n')
            file.write('<h1 style="text-align: center">{}测试报告</h1>\n'.format(project))
            file.write('<table style="width: 50%; margin: auto; text-align: center">\n')
            file.write('    <caption style="border-bottom: none; background-color: lightgray">\n')
            file.write(
                '        <div style="border-bottom: 1px solid gray; font-size: 1.5rem; font-weight: bold">概 述</div>\n')
            file.write('        <div style="padding: 0 5px; text-align: left">执行总数：{}</div>\n'.format(self.total_count))
            file.write('        <div style="padding: 0 5px; text-align: left">开始时间：{}&nbsp;&nbsp;&nbsp;&nbsp;结束时间：{}'
                       '&nbsp;&nbsp;&nbsp;&nbsp;执行耗时：{}</div>\n'.format(start_time, end_time, take_time))
            file.write('    </caption>\n')
            file.write('    <tr>\n')
            file.write('        <th style="width: 40%">执行结果</th>\n')
            file.write('        <th style="width: 30%">数量</th>\n')
            file.write('        <th style="width: 30%">百分比（%）</th>\n')
            file.write('    </tr>\n')
            file.write('    <tr>\n')
            file.write('        <td>通过</td>\n')
            file.write('        <td>{}</td>\n'.format(self.pass_count))
            file.write('        <td>{}</td>\n'.format(pass_percentage))
            file.write('    </tr>\n')
            file.write('    <tr>\n')
            file.write('        <td>失败</td>\n')
            file.write('        <td>{}</td>\n'.format(self.fail_count))
            file.write('        <td>{}</td>\n'.format(fail_percentage))
            file.write('    </tr>\n')
            file.write('    <tr>\n')
            file.write('        <td>阻塞</td>\n')
            file.write('        <td>{}</td>\n'.format(self.block_count))
            file.write('        <td>{}</td>\n'.format(block_percentage))
            file.write('    </tr>\n')
            file.write('    <tr>\n')
            file.write('        <td>超时</td>\n')
            file.write('        <td>{}</td>\n'.format(self.timeout_count))
            file.write('        <td>{}</td>\n'.format(timeout_percentage))
            file.write('    </tr>\n')
            file.write('    <tr>\n')
            file.write('        <td>未执行</td>\n')
            file.write('        <td>{}</td>\n'.format(self.not_executed_count))
            file.write('        <td>{}</td>\n'.format(not_executed_percentage))
            file.write('    </tr>\n')
            file.write('</table>\n')
            file.write('<br>\n')
            file.write('<table style="width: 100%; text-align: center">\n')
            file.write('    <caption style="border-bottom: none; background-color: lightgray; font-size: 1.5rem; '
                       'font-weight: bold">详 情\n')
            file.write('    </caption>\n')
            file.write('    <tr>\n')
            file.write('        <th style="width: 20%">模块</th>\n')
            file.write('        <th style="width: 50%">标题</th>\n')
            file.write('        <th style="width: 5%">优先级</th>\n')
            file.write('        <th style="width: 10%">开始时间</th>\n')
            file.write('        <th style="width: 10%">结束时间</th>\n')
            file.write('        <th style="width: 5%">测试结果</th>\n')
            file.write('        <th style="display: none">详情</th>\n')
            file.write('    </tr>\n')
            # 生成每条测试用例的测试结果
            for test_case in self.test_cases:
                file.write('    <tr>\n')
                file.write('        <td style="text-align: left">{}</td>\n'.format(test_case.module))
                file.write('        <td style="text-align: left">{}</td>\n'.format(test_case.title))
                file.write('        <td>{}</td>\n'.format(test_case.priority.name))
                if test_case.result == TestCaseResult.PASS:
                    file.write('        <td>{}</td>\n'.format(test_case.start_time))
                    file.write('        <td>{}</td>\n'.format(test_case.stop_time))
                    file.write('        <td style="background-color: green">成功</td>\n')
                elif test_case.result == TestCaseResult.FAIL:
                    file.write('        <td>{}</td>\n'.format(test_case.start_time))
                    file.write('        <td>{}</td>\n'.format(test_case.stop_time))
                    file.write('        <td style="background-color: red; color: -webkit-link; cursor: pointer; '
                               'text-decoration: underline" onclick="openDetail(this)">失败</td>\n')
                elif test_case.result == TestCaseResult.BLOCK:
                    file.write('        <td>{}</td>\n'.format(test_case.start_time))
                    file.write('        <td>{}</td>\n'.format(test_case.stop_time))
                    file.write('        <td style="background-color: yellow; color: -webkit-link; cursor: pointer; '
                               'text-decoration: underline" onclick="openDetail(this)">阻塞</td>\n')
                elif test_case.result == TestCaseResult.TIMEOUT:
                    file.write('        <td>{}</td>\n'.format(test_case.start_time))
                    file.write('        <td>{}</td>\n'.format(test_case.stop_time))
                    file.write('        <td style="background-color: lightgray; color: -webkit-link; cursor: pointer; '
                               'text-decoration: underline" onclick="openDetail(this)">超时</td>\n')
                elif test_case.result == TestCaseResult.NOT_EXECUTED:
                    file.write('        <td>--</td>\n'.format(test_case.start_time))
                    file.write('        <td>--</td>\n'.format(test_case.stop_time))
                    file.write('        <td>未执行</td>\n')
                file.write('        <td style="display: none">{}</td>\n'.format(test_case.result_detail))
                file.write('    </tr>\n')
            file.writelines('''</table>
<div style="position: fixed; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); display: none" id="detail" onclick="closeDetail()">
    <div style="width: 80%; max-height: 80%; z-index: 1; margin: 5% auto; overflow: auto; background-color: white" onclick="event.cancelBubble = true">
        <pre style="margin: 1rem; color: red; font-weight: bold" id="detail-content"></pre>
        <div style="margin-bottom: 1rem; text-align: center">
            <button onclick="closeDetail()">关 闭</button>
        </div>
    </div>
</div>
<script>

    function openDetail(obj) {
        document.getElementById('detail-content').innerHTML = obj.nextElementSibling.innerHTML;
        document.getElementById('detail').style.display = 'inline';
    }

    function closeDetail() {
        document.getElementById('detail').style.display = 'none';
    }

</script>
</body>
</html>\n''')
