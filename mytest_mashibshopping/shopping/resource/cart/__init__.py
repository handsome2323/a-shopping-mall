from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')  # 创建蓝图
cart_api = Api(cart_bp)  # 创建蓝图中的资源API

# 使用我们自定义json格式，替代装饰器的写法
cart_api.representation('application/json')(output_json)

from shopping.resource.cart.cart_resource import *

cart_api.add_resource(Shopping_Cart, '/user_cart', endpoint='user_cart')


