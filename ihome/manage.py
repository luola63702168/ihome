# coding: utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from ihome import create_app,db

# 创建flask应用对象
app = create_app("develop")
manager = Manager(app)
Migrate(app, db)  # 绑定
manager.add_command("db", MigrateCommand)  # 添加迁移命令


if __name__ == '__main__':
    manager.run()








