# test_case.py
from time import sleep

from testauto import main
from testauto.case import TestCase, TestCasePriority
from testauto.util import parameterized, assert_raise, assert_not_raise


class TestCase001(TestCase):

    def test_case(self):
        print(self.__class__.__name__)


class TestCase002(TestCase001):

    def test_case(self):
        print(self.__class__.__name__)


class TestCase003:

    def test_case(self):
        print(self.__class__.__name__)


class TestCase004(TestCase):

    def setup(self):
        print('这是初始化操作')

    def test_case(self):
        print('这是测试用例')

    def teardown(self):
        print('这是清理操作')


class TestCase005(TestCase):
    title = '登录成功'
    priority = TestCasePriority.P1
    completed = False

    def test_case(self):
        pass


class TestCase006(TestCase):

    def test_case(self):
        sleep(5)


class TestCase007(TestCase):

    def test_case(self):
        sleep(5)


@parameterized(
    ('username', 'password'),
    [
        ('zhangsan', 'zhangsan123456'),
        ('lisi', 'lisi123456')
    ]
)
class TestCase008(TestCase):

    def test_case(self):
        username = self.get_param_value('username')
        password = self.get_param_value('password')
        print('我的用户名是：{}，我的密码是：{}！'.format(username, password))


class TestCase009(TestCase):
    module = 'TestCase009模块'
    title = 'TestCase009标题'

    def test_case(self):
        sleep(1)


class TestCase010(TestCase):
    module = 'TestCase010模块'
    title = 'TestCase010标题'

    def test_case(self):
        sleep(2)
        assert False


class TestCase011(TestCase):
    module = 'TestCase011模块'
    title = 'TestCase011标题'

    def test_case(self):
        sleep(3)
        raise RuntimeError('我是TestCase011，这是我抛的异常！')


class TestCase012(TestCase):
    title = '抛出异常成功'

    def test_case(self):
        assert_raise(self._callable_target, RuntimeError)

    def _callable_target(self):
        raise RuntimeError('TestCase012的异常')


class TestCase013(TestCase):
    title = '不抛出异常成功'

    def test_case(self):
        assert_not_raise(self._callable_target, ValueError)

    def _callable_target(self):
        raise RuntimeError('TestCase013的异常')


class TestCase014(TestCase):
    title = '抛出异常失败'

    def test_case(self):
        assert_raise(self._callable_target, ValueError)

    def _callable_target(self):
        raise RuntimeError('TestCase014的异常')


class TestCase015(TestCase):
    title = '不抛出异常失败'

    def test_case(self):
        assert_not_raise(self._callable_target, RuntimeError)

    def _callable_target(self):
        raise RuntimeError('TestCase015的异常')


if __name__ == '__main__':
    main()
