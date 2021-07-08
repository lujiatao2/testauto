import os
from abc import ABC, abstractmethod
from enum import Enum
from importlib import import_module, util
from inspect import getmembers, isclass
from typing import List

from .case import TestCase, TestCasePriority
from .util import handle_path


class OperationMethod(Enum):
    EQUAL = '等于'
    NOT_EQUAL = '不等于'
    CONTAINS = '包含'
    NOT_CONTAINS = '不包含'
    GREATER = '大于'
    GREATER_EQUAL = '大于等于'
    LESS = '小于'
    LESS_EQUAL = '小于等于'


class TestCaseFilter(ABC):
    """
    测试用例过滤器抽象类
    """

    def __init__(self, operation_method: OperationMethod):
        self.operation_method = operation_method

    @abstractmethod
    def filter(self, test_cases: List[TestCase]) -> List[TestCase]:
        pass


class TestCaseCompletedShouldBe(TestCaseFilter):

    def __init__(self, operation_method: OperationMethod, test_case_completed: bool):
        super().__init__(operation_method)
        self.test_case_completed = test_case_completed

    def filter(self, test_cases: List[TestCase]) -> List[TestCase]:
        if self.operation_method == OperationMethod.EQUAL:
            return [test_case for test_case in test_cases if test_case.completed == self.test_case_completed]
        elif self.operation_method == OperationMethod.NOT_EQUAL:
            return [test_case for test_case in test_cases if test_case.completed != self.test_case_completed]
        else:
            raise ValueError(f'不支持的操作方法：{self.operation_method.value}！')


class TestCasePriorityShouldBe(TestCaseFilter):

    def __init__(self, operation_method: OperationMethod, *test_case_priorities: TestCasePriority):
        super().__init__(operation_method)
        self.test_case_priorities = test_case_priorities

    def filter(self, test_cases: List[TestCase]) -> List[TestCase]:
        if self.operation_method == OperationMethod.EQUAL:
            if len(self.test_case_priorities) != 1:
                raise ValueError(f'操作方法{self.operation_method.value}不支持多个条件！')
            return [test_case for test_case in test_cases if test_case.priority == self.test_case_priorities[0]]
        elif self.operation_method == OperationMethod.NOT_EQUAL:
            if len(self.test_case_priorities) != 1:
                raise ValueError(f'操作方法{self.operation_method.value}不支持多个条件！')
            return [test_case for test_case in test_cases if test_case.priority != self.test_case_priorities[0]]
        elif self.operation_method == OperationMethod.CONTAINS:
            return [test_case for test_case in test_cases if test_case.priority in self.test_case_priorities]
        elif self.operation_method == OperationMethod.NOT_CONTAINS:
            return [test_case for test_case in test_cases if test_case.priority not in self.test_case_priorities]
        else:
            raise ValueError(f'不支持的操作方法：{self.operation_method.value}！')


class TestTask(ABC):
    """
    测试任务抽象类
    """

    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.test_case_filters: List[TestCaseFilter] = []

    @abstractmethod
    def add_test_case(self, test_case: TestCase):
        pass

    @abstractmethod
    def add_test_cases(self, *test_cases: TestCase):
        pass

    @abstractmethod
    def add_test_cases_by_classes(self, *class_names: str):
        pass

    @abstractmethod
    def add_test_cases_by_modules(self, *module_names: str):
        pass

    @abstractmethod
    def add_test_cases_by_files(self, *files: str):
        pass

    @abstractmethod
    def add_test_cases_by_paths(self, *paths: str):
        pass

    @abstractmethod
    def remove_test_case(self, test_case: TestCase):
        pass

    @abstractmethod
    def remove_test_cases(self, *test_cases: TestCase):
        pass

    @abstractmethod
    def add_filter(self, test_case_filter: TestCaseFilter):
        pass

    @abstractmethod
    def add_filters(self, *test_case_filters: TestCaseFilter):
        pass

    @abstractmethod
    def remove_filter(self, test_case_filter: TestCaseFilter):
        pass

    @abstractmethod
    def remove_filters(self, *test_case_filters: TestCaseFilter):
        pass

    @abstractmethod
    def filter_test_cases(self):
        """
        过滤测试用例：将不满足测试用例过滤器规则的测试用例过滤掉。
        :return:
        """
        pass

    @abstractmethod
    def clear_test_task(self):
        pass


class DefaultTestTask(TestTask):
    """
    默认测试任务实现类
    """

    def __init__(self):
        super().__init__()
        default_filter = TestCaseCompletedShouldBe(OperationMethod.EQUAL, True)
        self.test_case_filters: List[TestCaseFilter] = [default_filter]

    def add_test_case(self, test_case: TestCase):
        self.test_cases.append(test_case)

    def add_test_cases(self, *test_cases: TestCase):
        self.test_cases.extend(test_cases)

    def add_test_cases_by_classes(self, *class_names: str):
        """
        通过类名增加测试用例
        :param class_names: 类名，格式：path.to.module.Class
        :return:
        """
        for class_name in class_names:
            tmp_module = import_module('.'.join(class_name.split('.')[:-1]))
            tmp_class_str = class_name.split('.')[-1]
            if hasattr(tmp_module, tmp_class_str):
                tmp_class = getattr(tmp_module, tmp_class_str)
                if issubclass(tmp_class, TestCase):
                    self.add_test_cases(*self._gen_test_case_instances(tmp_class))
                else:
                    raise ValueError(f'{tmp_class_str}不是测试用例类！')
            else:
                raise ValueError(f'指定的类不存在：{tmp_class_str}！')

    def add_test_cases_by_modules(self, *module_names: str):
        """
        通过模块名增加测试用例
        :param module_names: 模块名，格式：path.to.module
        :return:
        """
        for module_name in module_names:
            tmp_module = import_module(module_name)
            tmp_classes = getmembers(tmp_module, isclass)  # 获取模块中的所有类
            for _, tmp_class in tmp_classes:
                if issubclass(tmp_class, TestCase) and tmp_class is not TestCase:  # 排除TestCase本身
                    self.add_test_cases(*self._gen_test_case_instances(tmp_class))

    def add_test_cases_by_files(self, *files: str):
        """
        通过文件增加测试用例
        :param files: 文件，格式：
            Windows：E:\\path\\to\\dictionary\\module.py
            macOS/Linux：/path/to/dictionary/module.py
        :return:
        """
        for _file in files:
            new_file = handle_path(_file)
            new_file_name = new_file.split(os.sep)[-1]
            if not new_file_name.endswith('.py') or new_file_name == '__init__.py':
                continue
            self._add_test_cases_by_file(new_file, new_file_name)

    def add_test_cases_by_paths(self, *paths: str):
        """
        通过路径增加测试用例
        :param paths: 路径，格式：
            Windows：E:\\path\\to\\dictionary
            macOS/Linux：/path/to/dictionary
        :return:
        """
        for path in paths:
            new_path = handle_path(path)
            for root_dir, _, file_names in os.walk(new_path):
                for file_name in file_names:
                    if not file_name.endswith('.py') or file_name == '__init__.py':
                        continue
                    file_path = os.path.join(root_dir, file_name)
                    self._add_test_cases_by_file(file_path, file_name)

    def _add_test_cases_by_file(self, file_path, file_name):
        """
        通过文件增加测试用例
        :param file_path: 文件全路径
        :param file_name: 文件名
        :return:
        """
        tmp_module_spec = util.spec_from_file_location(file_name[:-3], file_path)
        tmp_module = tmp_module_spec.loader.load_module(tmp_module_spec.name)
        tmp_classes = getmembers(tmp_module, isclass)  # 获取模块中的所有类
        for _, tmp_class in tmp_classes:
            if issubclass(tmp_class, TestCase) and tmp_class is not TestCase:  # 排除TestCase本身
                self.add_test_cases(*self._gen_test_case_instances(tmp_class))

    @staticmethod
    def _gen_test_case_instances(test_case):
        """
        生成测试用例实例：参数化测试时，配合@parameterized装饰器使用。
        :param test_case: 测试用例类
        :return:
        """
        if not issubclass(test_case, TestCase):
            raise ValueError('不是测试用例类！')
        param_names = getattr(test_case, '_param_names') if hasattr(test_case, '_param_names') else None
        param_values = getattr(test_case, '_param_values') if hasattr(test_case, '_param_values') else None
        if param_names and param_values:  # 测试用例有参数化数据
            # 类型检查：参数名类型应该为Tuple[str, ...]，参数值类型应该为List[tuple]。
            if isinstance(param_names, tuple) and isinstance(param_values, list):
                # 类型检查：每个参数名类型应该为str。
                if not all([isinstance(param_name, str) for param_name in param_names]):
                    raise ValueError('参数名不是字符串！')
                test_cases = list()
                for param_value in param_values:
                    if len(param_names) != len(param_value):
                        raise ValueError('参数名数量与参数值数量不匹配！')
                    if not isinstance(param_value, tuple):  # 类型检查：一组参数值类型应该为tuple。
                        raise ValueError('该组参数值不是元组！')
                    test_cases.append(test_case(param_names=param_names, param_values=param_value))
                return test_cases
            else:
                raise ValueError('参数名或参数值的类型错误！')
        elif not param_names and not param_values:  # 测试用例无参数化数据
            return [test_case()]
        else:
            raise ValueError('只有参数名或参数值！')

    def remove_test_case(self, test_case: TestCase):
        self.test_cases.remove(test_case)

    def remove_test_cases(self, *test_cases: TestCase):
        for test_case in test_cases:
            self.test_cases.remove(test_case)

    def add_filter(self, test_case_filter: TestCaseFilter):
        self.test_case_filters.append(test_case_filter)

    def add_filters(self, *test_case_filters: TestCaseFilter):
        self.test_case_filters.extend(test_case_filters)

    def remove_filter(self, test_case_filter: TestCaseFilter):
        self.test_case_filters.remove(test_case_filter)

    def remove_filters(self, *test_case_filters: TestCaseFilter):
        for test_case_filter in test_case_filters:
            self.test_case_filters.remove(test_case_filter)

    def filter_test_cases(self):
        for test_case_filter in self.test_case_filters:
            self.test_cases = test_case_filter.filter(self.test_cases)

    def clear_test_task(self):
        self.test_cases.clear()
        self.test_case_filters.clear()
