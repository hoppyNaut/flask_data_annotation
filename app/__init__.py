from flask import Flask#从flask包中导入Flask类
from config import Config

# 数据库所需包
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder='../templates', static_folder='../static')#将Flask类的实例 赋值给名为 app 的变量。这个实例成为app包的成员。
app.config.from_object(Config)

# 数据库对象
db = SQLAlchemy(app)
# 迁移引擎对象
migrate = Migrate(app, db)

from app import routes, models