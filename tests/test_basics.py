import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):  # setUp方法用于创建一个测试环境
        self.app = create_app('testing')  # 创建一个测试程序
        self.app_context = self.app.app_context()  # 激活上下文
        self.app_context.push()
        db.create_all()  # 创建一个全新的数据库

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # 删除这个测试数据库
        self.app_context.pop()  # 删除这个测试的程序上下文

    def test_app_exists(self):  # 确保程序实例存在
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):  # 确保程序在测试配置中运行
        self.assertTrue(current_app.config['TESTING'])
