from testauto.util import assert_raise, assert_not_raise


def callable_func():
    raise RuntimeError


if __name__ == '__main__':
    assert_raise(callable_func, RuntimeError)
    assert_raise(callable_func, ValueError, msg='没有抛出RuntimeError异常！')
    assert_not_raise(callable_func, ValueError)
