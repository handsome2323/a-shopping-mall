from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

address_bp = Blueprint('address', __name__, url_prefix='/address')  # 创建蓝图
address_api = Api(address_bp)  # 创建蓝图中的资源API

# 使用我们自定义json格式，替代装饰器的写法
address_api.representation('application/json')(output_json)

from shopping.resource.address.address_resource import *

address_api.add_resource(User_Address, '/user_address', endpoint='user_address')


