from setuptools import setup

with open('README.md', 'r', encoding='UTF-8') as file:
    long_description = file.read()

setup(
    name='test-auto',
    version='1.0.0',
    description='Python软件自动化测试框架，支持多线程和参数化测试，且自带HTML测试报告！',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='卢家涛',
    author_email='522430860@qq.com',
    url='https://github.com/lujiatao2',
    packages=['testauto', 'testauto_test']
)
