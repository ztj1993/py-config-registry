# -*- coding: utf-8 -*-

import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()
readme = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='config-registry',
    version='1.0.0',
    description='python config registry package',
    long_description=readme,
    long_description_content_type='text/markdown',
    py_modules=['ConfigRegistry'],
    url='https://pypi.org/project/config-registry',
    author='ZhangTianJie',
    author_email='ztj1993@gmail.com',
    keywords='registry config json yaml',
    license='MIT License',
)
