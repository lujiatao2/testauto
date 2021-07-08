# case_for_doc.py
from time import sleep

from testauto import main
from testauto.case import TestCase, TestCasePriority
from testauto.util import parameterized, assert_raise, assert_not_raise


class TestCase01(TestCase):

    def test_case(self):
        ...


class TestCase02(TestCase):

    def test_case(self):
        print(self.__class__.__name__)


class TestCase03(TestCase02):

    def test_case(self):
        print(self.__class__.__name__)


class TestCase04:

    def test_case(self):
        print(self.__class__.__name__)


class TestCase05(TestCase):

    def setup(self):
        print('这是初始化操作')

    def test_case(self):
        print('这是测试用例')

    def teardown(self):
        print('这是清理操作')


class TestCase06(TestCase):
    title = '登录成功'
    priority = TestCasePriority.P1
    completed = False

    def test_case(self):
        ...


class TestCase07(TestCase):

    def test_case(self):
        sleep(5)


class TestCase08(TestCase):

    def test_case(self):
        sleep(5)


@parameterized(
    ('username', 'password'),
    [
        ('zhangsan', 'zhangsan123456'),
        ('lisi', 'lisi123456')
    ]
)
class TestCase09(TestCase):

    def test_case(self):
        username = self.get_param_value('username')
        password = self.get_param_value('password')
        print(f'我的用户名是：{username}，我的密码是：{password}！')


class TestCase10(TestCase):
    module = 'TestCase10模块'
    title = 'TestCase10标题'

    def test_case(self):
        sleep(1)


class TestCase11(TestCase):
    module = 'TestCase11模块'
    title = 'TestCase11标题'

    def test_case(self):
        sleep(2)
        assert False


class TestCase12(TestCase):
    module = 'TestCase12模块'
    title = 'TestCase12标题'

    def test_case(self):
        sleep(3)
        raise RuntimeError('我是TestCase12，这是我抛的异常！')


class TestCase13(TestCase):
    title = '抛出异常成功'

    def test_case(self):
        assert_raise(self._callable_target, RuntimeError)

    def _callable_target(self):
        raise RuntimeError('TestCase13的异常')


class TestCase14(TestCase):
    title = '不抛出异常成功'

    def test_case(self):
        assert_not_raise(self._callable_target, ValueError)

    def _callable_target(self):
        raise RuntimeError('TestCase14的异常')


class TestCase15(TestCase):
    title = '抛出异常失败'

    def test_case(self):
        assert_raise(self._callable_target, ValueError)

    def _callable_target(self):
        raise RuntimeError('TestCase15的异常')


class TestCase16(TestCase):
    title = '不抛出异常失败'

    def test_case(self):
        assert_not_raise(self._callable_target, RuntimeError)

    def _callable_target(self):
        raise RuntimeError('TestCase16的异常')


if __name__ == '__main__':
    main()
