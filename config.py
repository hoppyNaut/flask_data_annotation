import os

# 获取当前.py文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 表单配置项
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
    # 数据库配置项
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False