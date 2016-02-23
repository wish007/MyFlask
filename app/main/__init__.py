from flask import Blueprint

main = Blueprint('main', __name__)  # 实例化一个Blueprint类对象来创建蓝本

from . import views, errors  # 导入views、errors模块把路由、错误处理和蓝本关联起来
