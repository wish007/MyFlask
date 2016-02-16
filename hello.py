# 使用render_template函数把JinJa2模板引擎集成到hello.py
# render-传递，template-模板
from flask import Flask, render_template, session, redirect, url_for, flash
# 将Flask-Bootstrap从flask.ext命名空间导入
from flask.ext.bootstrap import Bootstrap
# 导入和表单提交有关的类
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
# 导入os模块
import os
# 导入ORM数据库框架SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
# 用Flask-Script的shell命令自动导入数据库实例和模型
from flask.ext.script import Manager, Shell
# 导入数据库迁移的类
from flask.ext.migrate import Migrate, MigrateCommand
# 初始化Flask-Mail
from flask.ext.mail import Mail, Message
# 导入线程类，这里用于异步发送电子邮件
from threading import Thread

# 与数据库有关
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# 使用Flask-WTF设置一个密钥，避免跨站请求伪造攻击
app.config['SECRET_KEY'] = 'hard to guess string'
# 数据库相关配置
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 配置Flask-Mail,此处填了专门注册的测试邮箱myflask@163.com
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
# 从环境变量中获取邮件的用户名和密码
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# 定义邮件主题的前缀
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# 定义发件人地址
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <zyoutong@163.com>'
# 获取收件人邮箱地址，这里获取的是管理员邮箱
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

manager = Manager(app)
# 将程序实例传入构造方法进行初始化
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# 在视图函数
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# 自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# 定义一个异步发送电子邮件的函数
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# 定义一个发送电子邮件的函数
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

# 为shell命令添加上下文
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# 定义一个表单类，用于提交表单
class NameForm(Form):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')


# 定义Role模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 表示Role和User的一对多关系
    users = db.relationship('User', backref='role', lazy='dynamic')

    # 定义__repr__方法，返回一个具有可读性的字符串表示模型，可在调试和测试时使用
    def __repr__(self):
        return '<Role %r>' % self.name


# 定义User模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 表示Role和User的一对多关系
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # 定义__repr__方法，返回一个具有可读性的字符串表示模型，可在调试和测试时使用
    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
    # 用run方法启动Flask集成的Web服务器，并启用调试模式
    manager.run()
