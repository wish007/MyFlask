import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:  # 定义程序的通用配置类
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'  # 使用Flask-WTF设置一个密钥，避免跨站请求伪造攻击
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'  # 发邮件的服务器
    MAIL_PORT = 25  # 163邮箱的smtp协议端口
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 从环境变量中获取邮箱的用户名
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 从环境变量中获取邮箱的密码
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'  # 定义邮件主题的前缀
    FLASKY_MAIL_SENDER = 'Flasky Admin <zyoutong@163.com>'  # 定义发件人地址
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')  # 自定义管理员的收件邮箱

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):  # 定义继承Config类的开发配置类
    DEBUG = True  # 开启debug模式
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')  # 为不同的环境指定不同的数据库文件


class TestingConfig(Config):  # 定义继承Config类的测试配置类
    TESTING = True  # 开启testing模式
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')  # 为不同的环境指定不同的数据库文件


class ProductionConfig(Config):  # 定义继承Config类的生成环境配置类
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')  # 为不同的环境指定不同的数据库文件


config = {  # 注册不同的配置环境
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig  # 注册默认的配置
}
