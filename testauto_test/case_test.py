from testauto import main
from testauto.case import TestCase
from testauto.util import parameterized


# 不带初始化和清理操作的测试用例
class TestCase01(TestCase):

    def test_case(self):
        print('TestCase01')


# 非测试用例
class TestCase02:

    def test_case(self):
        print('TestCase02')


# 带初始化和清理操作的测试用例
class TestCase03(TestCase):

    def setup(self):
        print('TestCase03 - setup')

    def test_case(self):
        print('TestCase03')

    def teardown(self):
        print('TestCase03 - teardown')


# 正确的参数化测试用例
@parameterized(
    ('username', 'password'),
    [
        ('zhangsan', 'zhangsan123456'),
        ('lisi', 'lisi123456')
    ]
)
class TestCase04(TestCase):

    def test_case(self):
        username = self.get_param_value('username')
        password = self.get_param_value('password')
        print(f'我的用户名是：{username}，我的密码是：{password}！')


# 异常的参数化测试用例
@parameterized(
    ('username', 'password'),
    [
        ('zhangsan', 'zhangsan123456', 111),
        ('lisi', 'lisi123456', 222)
    ]
)
class TestCase05(TestCase):

    def test_case(self):
        username = self.get_param_value('username')
        password = self.get_param_value('password')
        print(f'我的用户名是：{username}，我的密码是：{password}！')


if __name__ == '__main__':
    main()
