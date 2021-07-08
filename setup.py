from setuptools import setup

with open('README.md', 'r', encoding='UTF-8') as file:
    long_description = file.read()

setup(
    name='test-auto',
    version='1.0.2',
    description='自动化测试框架，支持多线程和参数化测试，且自带HTML测试报告！',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='卢家涛',
    author_email='522430860@qq.com',
    url='https://github.com/lujiatao2',
    packages=['testauto', 'testauto_test'],
    license="MIT",
    project_urls={
        'Source': 'https://github.com/lujiatao2/testauto',
        'Changelog': 'https://github.com/lujiatao2/testauto/blob/master/CHANGELOG.md'
    },
    classifiers=[
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Unit',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)'
    ]
)
