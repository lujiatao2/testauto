&emsp;&emsp;自动化测试框架，支持多线程和参数化测试，且自带HTML测试报告！

# 主要特性

* 支持IDE和命令行方式执行测试用例。
* 支持多线程测试。
* 支持参数化测试。
* 自带HTML测试报告。
* 支持设置终止策略、重试策略和超时时间。
* 易扩展，开发者可自定义测试任务、测试记录器和测试执行器等。

# 安装

## 在线安装

&emsp;&emsp;执行以下命令即可安装testauto的最新版本：

```
pip install test-auto
```

&emsp;&emsp;如需安装指定版本，比如安装1.0.0版本，可执行以下命令：

```
pip install test-auto==1.0.0
```

## 离线安装

&emsp;&emsp;如果已经下载了test_auto-X.X.X-py3-none-any.whl或test-auto-X.X.X.tar.gz安装文件，那么可以使用离线安装方式安装testauto。  
&emsp;&emsp;你可以在PyPI的以下地址找到安装文件：

```
https://pypi.org/project/test-auto/#files
```

&emsp;&emsp;或者GitHub的以下地址找到安装文件：

```
https://github.com/lujiatao2/testauto/releases
```

&emsp;&emsp;若使用test_auto-X.X.X-py3-none-any.whl安装文件，执行以下命令即可安装testauto：

```
pip install path/to/test_auto-X.X.X-py3-none-any.whl
```

&emsp;&emsp;若使用test-auto-X.X.X.tar.gz安装文件，执行以下命令即可安装testauto：

```
pip install path/to/test-auto-X.X.X.tar.gz
```

# 第一个测试用例

&emsp;&emsp;来开始使用testauto编写第一个测试用例吧！

```python
# case_for_doc.py
from testauto import main
from testauto.case import TestCase


class TestCase01(TestCase):

    def test_case(self):
        ...


if __name__ == '__main__':
    main()

```

&emsp;&emsp;执行结果如下：

```
======================================================================================================================================================
执行总数：1
开始时间：2021-01-24 14:48:21    结束时间：2021-01-24 14:48:21    执行耗时：00时00分00秒
------------------------------------------------------------------------------------------------------------------------------------------------------
执行结果      数量        百分比（%）
通过        1         100.0
失败        0         0.0
阻塞        0         0.0
超时        0         0.0
未执行       0         0.0
======================================================================================================================================================

```

# 测试用例

## 基本用法

&emsp;&emsp;测试用例使用一个Python类来表示，且该类必须直接或间接继承至TestCase抽象基类才能被testauto识别为测试用例。

```python
class TestCase02(TestCase):

    def test_case(self):
        print(self.__class__.__name__)


class TestCase03(TestCase02):

    def test_case(self):
        print(self.__class__.__name__)


class TestCase04:

    def test_case(self):
        print(self.__class__.__name__)

```

&emsp;&emsp;执行以上代码后，可以看到只有TestCase02和TestCase03的类名被打印了。

## 初始化和清理操作

&emsp;&emsp;测试用例支持添加初始化和清理操作，只需重写setup()和teardown()方法即可。

```python
class TestCase05(TestCase):

    def setup(self):
        print('这是初始化操作')

    def test_case(self):
        print('这是测试用例')

    def teardown(self):
        print('这是清理操作')

```

&emsp;&emsp;执行结果如下：

```
这是初始化操作
这是测试用例
这是清理操作
```

## 测试用例属性

* project：测试工程名称，默认为：Default Project。
* module：测试模块名称，默认为：Default Module。
* title：测试用例标题，默认为：Default Title。
* description：测试用例描述，默认：无。
* priority：测试用例优先级，默认：P0。
* designer：测试用例设计者，默认：Anonymous。
* version：测试用例版本号，默认：1.0.0。
* completed：测试用例完成状态，默认：已完成。

&emsp;&emsp;以上属性都可以修改，只需在测试用例中显式声明即可。

```python
class TestCase06(TestCase):
    title = '登录成功'
    priority = TestCasePriority.P1
    completed = False

    def test_case(self):
        ...

```

&emsp;&emsp;从以上代码可以看出：测试用例优先级使用枚举表示，而不是字符串；而测试用例完成状态是一个布尔类型。

# 测试任务

## 基本用法

&emsp;&emsp;testauto的执行单元是测试任务，而不是测试用例，即使只有一个测试用例，testauto也会自动将该测试用例转换为测试任务。  
&emsp;&emsp;为什么需要测试任务？比如一个测试项目有1000个测试用例，但对于不同的测试策略（冒烟测试？回归测试？），需要执行的测试用例显然是不同的，因此我们可以创建不同的测试任务。

```python
# task_for_doc.py
from testauto.task import DefaultTestTask

from testauto_test.case_for_doc import *

# 冒烟测试用例对应的测试任务
test_task_01 = DefaultTestTask()
test_task_01.add_test_cases(TestCase01(), TestCase02())

# 回归测试用例对应的测试任务
test_task_02 = DefaultTestTask()
test_task_02.add_test_cases(TestCase01(), TestCase03())

if __name__ == '__main__':
    main(test_task=test_task_01)  # 执行冒烟测试
    main(test_task=test_task_02)  # 执行回归测试

```

&emsp;&emsp;以上代码中的测试用例是上一节case_for_doc.py中的测试用例。

## 添加测试用例

&emsp;&emsp;除了上一小节介绍的add_test_cases()方法外，还支持多种添加测试用例方法，以下为完整列表：

* add_test_case()：添加单个测试用例。
* add_test_cases()：添加多个测试用例。
* add_test_cases_by_classes()：通过类名增加测试用例，格式：path.to.module.Class
* add_test_cases_by_modules()：通过模块名增加测试用例，格式：path.to.module
* add_test_cases_by_files()：通过文件增加测试用例，格式：  
  Windows：E:\\path\\to\\dictionary\\module.py  
  macOS/Linux：/path/to/dictionary/module.py
* add_test_cases_by_paths()：通过路径增加测试用例，格式：  
  Windows：E:\\path\\to\\dictionary  
  macOS/Linux：/path/to/dictionary

&emsp;&emsp;以下演示add_test_cases_by_files()方法的使用：

```python
test_task_03 = DefaultTestTask()
test_task_03.add_test_cases_by_files(
    r'E:\Software_Testing\Software Development\Python\PycharmProjects\testauto\testauto_test\case_for_doc.py')

if __name__ == '__main__':
    main(test_task=test_task_03)

```

&emsp;&emsp;除了添加，也可以删除测试用例，对应的方法是remove_test_case()和remove_test_cases()。

## 过滤器

&emsp;&emsp;过滤器是一个抽象类TestCaseFilter，它的作用是过滤掉不满足要求的测试用例。testauto内置了2个过滤器：

* TestCaseCompletedShouldBe：根据测试用例完成状态来过滤测试用例。
* TestCasePriorityShouldBe：根据测试用例优先级来过滤测试用例。

&emsp;&emsp;比如我们只想执行P0优先级的测试用例，可以这么做：

```python
test_task_03 = DefaultTestTask()
test_task_03.add_test_cases_by_files(
    r'E:\Software_Testing\Software Development\Python\PycharmProjects\testauto\testauto_test\case_for_doc.py')
test_task_03.add_filter(TestCasePriorityShouldBe(OperationMethod.EQUAL, TestCasePriority.P0))
test_task_03.filter_test_cases()

if __name__ == '__main__':
    main(test_task=test_task_03)

```

&emsp;&emsp;从以上代码可以看出：在添加了过滤器后，要真正执行过滤操作，需要调用filter_test_cases()方法。  
&emsp;&emsp;除了添加，也可以删除过滤器，对应的方法是remove_test_filter()和remove_test_filters()。  
&emsp;&emsp;另外，DefaultTestTask默认包含TestCaseCompletedShouldBe过滤器，且过滤条件为OperationMethod.EQUAL和True，即测试用例完成状态等于True的测试用例才会被保留。当然你可以调用clear_test_task()
方法来阻止该行为，该方法会清空测试任务中的所有测试用例和过滤器。

# 命令行执行

&emsp;&emsp;testauto提供了命令行执行的功能，执行以下命令获取帮助信息：

```
python -m testauto -h
```

&emsp;&emsp;执行结果如下：

```
usage: testauto [-h] [-m [TEST_MODULES [TEST_MODULES ...]]] [-t TEST_TASK]
                [-r TEST_RECORDER] [-rn TEST_RUNNER] [-s STOP_STRATEGY]
                [-rt RETRY_STRATEGY] [-to TIMEOUT] [-p PARALLEL]

optional arguments:
  -h, --help            显示帮助信息。
  -m [TEST_MODULES [TEST_MODULES ...]], --test-modules [TEST_MODULES [TEST_MODULES ...]]
                        测试模块。示例：-m E:\path\to\dictionary\module.py
  -t TEST_TASK, --test-task TEST_TASK
                        测试任务。示例：-t path.to.module.callable，其中callable为返回TestTask对象的可调用对象。
  -r TEST_RECORDER, --test-recorder TEST_RECORDER
                        测试记录器。示例：-r path.to.module.callable，其中callable为返回TestRecorder对象的可调用对象。
  -rn TEST_RUNNER, --test-runner TEST_RUNNER
                        测试执行器。示例：-rn path.to.module.callable，其中callable为返回TestRunner对象的可调用对象。
  -s STOP_STRATEGY, --stop-strategy STOP_STRATEGY
                        终止策略。参数取值：0-全部完成（默认）/1-第一个未执行成功/2-第一个P0测试用例未执行成功
  -rt RETRY_STRATEGY, --retry-strategy RETRY_STRATEGY
                        重试策略。参数取值：0-不重试（默认）/1-立即重新执行测试用例/2-最后重新执行测试用例
  -to TIMEOUT, --timeout TIMEOUT
                        超时时间（单位秒）。参数取值：正整数
  -p PARALLEL, --parallel PARALLEL
                        并行执行数量。参数取值：正整数

```

&emsp;&emsp;以上帮助信息已经把使用方法说明得很清楚了，以下演示如何使用命令行执行测试任务，新增测试任务test_task_04：

```python
def test_task_04():
    test_task = DefaultTestTask()
    test_task.add_test_cases(TestCase01(), TestCase02())
    return test_task

```

&emsp;&emsp;注意test_task_04要定义为可调用对象，这里定义为了一个函数。  
&emsp;&emsp;执行以下命令可运行test_task_04中的测试用例：

```
python -m testauto -t testauto_test.test_task.test_task_04
```

&emsp;&emsp;另外，IDE和命令行均支持直接传入测试模块，但此时若同时传入了测试任务，testauto会忽略测试任务，而使用传入的测试模块自动创建测试任务。

# 多线程测试

&emsp;&emsp;testauto支持多线程测试，使用方法很简单，通过main()方法传入parallel参数或命令行传入-p/--parallel参数即可。  
&emsp;&emsp;为了演示多线程测试带来的效率上优势，我们首先在case_for_doc.py中新增以下两个测试用例：

```python
class TestCase07(TestCase):

    def test_case(self):
        sleep(5)


class TestCase08(TestCase):

    def test_case(self):
        sleep(5)

```

&emsp;&emsp;然后在task_for_doc.py中新增test_task_05：

```python
test_task_05 = DefaultTestTask()
test_task_05.add_test_cases(TestCase07(), TestCase08())

if __name__ == '__main__':
    main(test_task=test_task_05)

```

&emsp;&emsp;如果直接执行test_task_05，那么测试耗时是10秒，这时我们加入parallel参数，并将参数值设置为2：

```python
if __name__ == '__main__':
    main(test_task=test_task_05, parallel=2)

```

&emsp;&emsp;重新执行test_task_05，可以看到耗时为5秒。  
&emsp;&emsp;需要注意的是，多线程执行测试用例时，需考虑线程安全性，如果多个测试用例同时对一个资源进行修改，会造成意想不到的结果。

# 参数化测试

&emsp;&emsp;testauto使用@parameterized装饰器提供对参数化的支持。  
&emsp;&emsp;首先在case_for_doc.py中新增以下测试用例：

```python
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

```

&emsp;&emsp;@parameterized装饰器的第一个参数是一个字符串类型的元组，每个字符串代表一个参数，可传递多个参数；第二个参数是一个元组组成的列表，每个元组代表一组参数，元组中参数的个数必须与参数数量一致。然后在测试用例中通过get_param_value()
方法来获取参数。  
&emsp;&emsp;在test_task.py中新增test_task_06：

```python
test_task_06 = DefaultTestTask()
test_task_06.add_test_cases_by_classes('testauto_test.case_for_doc.TestCase09')

if __name__ == '__main__':
    main(test_task=test_task_06)

```

&emsp;&emsp;注意test_task_06添加测试用例的方式不是直接传递测试用例对象，因为参数化测试时，需要根据参数的数量来动态创建测试用例对象，这个过程是testauto自动完成的。  
&emsp;&emsp;执行结果如下：

```
我的用户名是：zhangsan，我的密码是：zhangsan123456！
我的用户名是：lisi，我的密码是：lisi123456！
```

# 测试报告

&emsp;&emsp;testauto有5种测试结果：

* 通过：未引发任何异常。
* 失败：引发AssertionError异常。
* 超时：引发TimeoutError异常。
* 阻塞：引发其它异常（非AssertionError和TimeoutError异常）。
* 未执行：未执行。

&emsp;&emsp;testauto内置的测试记录器DefaultTestRecorder会生成HTML测试报告。  
&emsp;&emsp;为了查看不同测试结果在测试报告中的显示效果，在case_for_doc.py中新增以下3个测试用例：

```python
class TestCase010(TestCase):
    module = 'TestCase010模块'
    title = 'TestCase010标题'

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

```

&emsp;&emsp;然后直接执行test_task_03，执行后会生成test-report.html文件，该文件即HTML测试报告。效果如下所示：
![HTML测试报告01](https://raw.githubusercontent.com/lujiatao2/testauto/master/testauto_test/HTML%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A01.png)
&emsp;&emsp;未执行成功的测试用例，可点击查看详情，效果如下所示：
![HTML测试报告02](https://raw.githubusercontent.com/lujiatao2/testauto/master/testauto_test/HTML%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A02.png)
&emsp;&emsp;不同的测试结果在HTML测试报告中显示是不同的：

* 通过：显示为绿色，不能点击详情查看。
* 失败：显示为红色，能点击详情查看。
* 阻塞：显示为黄色，能点击详情查看。
* 超时：显示为灰色，能点击详情查看。
* 未执行：显示为白色，不能点击详情查看。

# 其它

## 终止策略

&emsp;&emsp;testauto支持3种终止策略：

* ALL_COMPLETED：全部完成，默认。
* FIRST_NOT_PASS：第一个未执行成功。
* FIRST_P0_NOT_PASS：第一个P0测试用例未执行成功。

&emsp;&emsp;终止策略使用StopStrategy枚举来设置：

```python
if __name__ == '__main__':
    main(stop_strategy=StopStrategy.FIRST_NOT_PASS)

```

## 重试策略

&emsp;&emsp;testauto支持3种重试策略：

* NOT_RERUN：不重试，默认。
* RERUN_NOW：立即重新执行测试用例，即：对当前未执行成功的测试用例，立即重新执行一次。
* RERUN_LAST：最后重新执行测试用例，即：对全部未执行成功的测试用例，最后批量重新执行一次。

&emsp;&emsp;重试策略使用RetryStrategy枚举来设置：

```python
if __name__ == '__main__':
    main(retry_strategy=RetryStrategy.RERUN_NOW)

```

&emsp;&emsp;注意终止策略的优先级是大于重试策略的，比如同时设置了FIRST_NOT_PASS和RERUN_NOW，当测试用例执行失败时，testauto会立即终止后续测试用例的执行，而不会对当前测试用例进行重新执行。

## 超时时间

&emsp;&emsp;使用timeout参数可对单个测试用例设置超时时间：

```python
if __name__ == '__main__':
    main(timeout=60)

```

&emsp;&emsp;以上代码将单个测试用例的执行超时时间设置为了60秒，默认为1小时（3600秒）。

## 断言

&emsp;&emsp;作为自动化测试框架，断言功能当然是不能少的，但testauto没有重复造轮子，而是直接使用Python自带的assert关键字来实现断言。比如TestCase11测试用例中断言的写法如下：

```python
class TestCase11(TestCase):
    module = 'TestCase11模块'
    title = 'TestCase11标题'

    def test_case(self):
        sleep(2)
        assert False

```

&emsp;&emsp;以上代码直接使用了assert关键字来断言。  
&emsp;&emsp;但testauto也新增了2个断言函数作为补充：

* assert_raise()：断言抛出指定异常。
* assert_not_raise()：断言不抛出指定异常。

&emsp;&emsp;以下为演示代码，可参考这几个测试用例的写法来使用以上断言函数：

```python
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

```