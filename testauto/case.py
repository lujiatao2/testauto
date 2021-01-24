from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple


class TestCasePriority(Enum):
    P0 = '冒烟测试用例'
    P1 = '核心测试用例'
    P2 = '普通测试用例'
    P3 = '次要测试用例'


class TestCaseResult(Enum):
    NOT_EXECUTED = '未执行'
    EXECUTING = '执行中'
    PASS = '成功'
    FAIL = '失败'
    BLOCK = '阻塞'
    TIMEOUT = '超时'


class TestCase(ABC):
    """
    测试用例抽象类：测试用例类必须继承至它。
    """

    project = 'Default Project'
    module = 'Default Module'
    title = 'Default Title'
    description = ''
    priority = TestCasePriority.P0
    designer = 'Anonymous'
    version = '1.0.0'
    completed = True  # 测试用例完成状态：True-已完成/False-未完成（草拟中）

    def __init__(self, param_names: Tuple[str, ...] = None, param_values: tuple = None):
        """
        :param param_names: 参数名：参数化测试时，配合@parameterized装饰器使用。
        :param param_values: 参数值：参数化测试时，配合@parameterized装饰器使用。
        """
        self.start_time = ''
        self.stop_time = ''
        self.result = TestCaseResult.NOT_EXECUTED
        self.result_detail = ''
        builtin_instance_attr = self.__dict__.keys()
        if param_names and param_values:
            if len(param_names) != len(param_values):
                raise ValueError('参数名数量与参数值数量不匹配！')
            for i in range(len(param_names)):
                if param_names[i] in builtin_instance_attr:
                    raise ValueError('参数名与内置的实例属性名冲突了！')
                self.__dict__[param_names[i]] = param_values[i]  # 动态添加实例属性
        elif not param_names and not param_values:
            pass
        else:
            raise ValueError('只有参数名或参数值！')

    def setup(self):
        """
        测试用例前置条件（初始化操作）
        :return:
        """
        pass

    @abstractmethod
    def test_case(self):
        """
        测试用例
        :return:
        """
        pass

    def teardown(self):
        """
        测试用例后置条件（清理操作）
        :return:
        """
        pass

    def get_param_value(self, param_name: str):
        """
        获取参数值：参数化测试时，获取@parameterized装饰器传入的参数对应的参数值。
        :param param_name: 参数名
        :return:
        """
        try:
            return self.__dict__[param_name]
        except KeyError:
            raise ValueError('没有该参数：{}！'.format(param_name))
