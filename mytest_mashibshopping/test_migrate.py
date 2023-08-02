#通过执行命令创建数据的表
from flask_migrate import Migrate,MigrateCommand

from flask_script import Manager

from shopping import creat_app

# from comment.models.payment import *

# from comment .models import *

from comment.models.person import *
#初始化app
app = creat_app('develop')

manager=Manager(app)

Migrate(app,db)
manager.add_command('shopping_db',MigrateCommand)

if __name__ == '__main__':
    manager.run()