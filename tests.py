# -*- coding: utf-8 -*-
# Intro: 配置模块单元测试

import time
import unittest

from ConfigRegistry import ConfigRegistry


class TestConfigRegistry(unittest.TestCase):

    def test_init(self):
        """测试初始化"""
        setting = ConfigRegistry({'a': {'aa': 'aaa'}})
        self.assertEqual(setting.get(), {'a': {'aa': 'aaa'}})
        self.assertEqual(setting.get('a.aa'), 'aaa')

    def test_set(self):
        """测试设置配置项"""
        setting = ConfigRegistry()
        setting.set('a', 'a')
        setting.set('b', [1, 2])
        setting.set('c.h', 'h')
        self.assertEqual(setting.get(), {
            'a': 'a',
            'b': [1, 2],
            'c': {
                'h': 'h'
            }
        })

    def test_unset(self):
        """测试删除配置项"""
        setting = ConfigRegistry()
        setting.set('a', 'a')
        setting.set('b', [1, 2])
        setting.set('c.i.h', 'h')
        setting.set('c.i.j', 'j')
        setting.unset('c.i.h')
        self.assertEqual(setting.get(), {
            'a': 'a',
            'b': [1, 2],
            'c': {
                'i': {
                    'j': 'j'
                }
            }
        })
        setting.unset('c.i.j', clear=True)
        self.assertEqual(setting.get(), {
            'a': 'a',
            'b': [1, 2]
        })

    def test_flat(self):
        """测试扁平处理"""
        setting = ConfigRegistry({
            'a': {
                'h': 'h',
                'i': 'i',
            }
        })
        self.assertEqual(setting.flat(), {
            'a.h': 'h',
            'a.i': 'i',
        })

    def test_merge(self):
        """测试合并配置"""
        setting = ConfigRegistry({
            'a': {
                'h': 'h',
                'i': 'i',
            }
        })
        setting.merge({
            'a': {
                'g': 'g',
            }
        })
        self.assertEqual(setting.get(), {
            'a': {
                'h': 'h',
                'i': 'i',
                'g': 'g',
            }
        })

    def test_get(self):
        """测试获取配置项"""
        setting = ConfigRegistry({'a': {'aa': 'aaa'}})
        self.assertEqual(setting.get(), {'a': {'aa': 'aaa'}})
        self.assertEqual(setting.get('a'), {'aa': 'aaa'})
        self.assertEqual(setting.get('a.aa'), 'aaa')
        self.assertEqual(setting.get('b', ['b']), ['b'])

    def test_append(self):
        """测试列表追加值"""
        setting = ConfigRegistry({'a': {'b': ['c', 'd']}})
        setting.append('a.b', 'e')
        self.assertEqual(setting.get(), {'a': {'b': ['c', 'd', 'e']}})

    def test_default(self):
        """测试设置默认值"""
        setting = ConfigRegistry({'a': 'aaa'})
        self.assertEqual(setting.default('a', 'bbb'), 'aaa')
        self.assertEqual(setting.get('a'), 'aaa')
        self.assertEqual(setting.default('c', 'ccc'), 'ccc')
        self.assertEqual(setting.get('c', 'ccc'), 'ccc')

    def test_load(self):
        """测试加载配置项"""
        d = {
            'a': 'a',
            'b': 1,
            'c': {
                'h': 'h',
            },
            'd': [1, 2],
            'e': True,
            'f': 1.1,
        }
        setting = ConfigRegistry()
        setting.load(d)
        self.assertEqual(setting.get(), d)

    def test_hook(self):
        """测试钩子"""
        setting = ConfigRegistry()

        def callback():
            setting.set('a', 'aaa')
            return True

        setting.setting_hook('hook', 3, callback)
        time.sleep(1)
        setting.refresh_hook('hook')
        self.assertEqual(setting.get('a'), None)
        time.sleep(3)
        setting.refresh_hook('hook')
        self.assertEqual(setting.get('a'), 'aaa')


if __name__ == '__main__':
    unittest.main()
