#冬宝商城项目的入口
from flask import Flask

from shopping import creat_app

from setting import map_config

from flask_wtf.csrf import CSRFProtect

import sys

import os

path=os.path.dirname(sys.path[0])

if path and path not in sys.path:
    print('>>>>>>>>>这是path',path)
app=creat_app('develop')
# csrf = CSRFProtect(app)
if __name__ == '__main__':
    app.run()
