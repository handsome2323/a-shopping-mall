from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

coupon_bp = Blueprint('coupon', __name__, url_prefix='/coupon')  # 创建蓝图
coupon_api = Api(coupon_bp)  # 创建蓝图中的资源API

# 使用我们自定义json格式，替代装饰器的写法
coupon_api.representation('application/json')(output_json)

from shopping.resource.coupon.coupon_resource import *

coupon_api.add_resource(Coupon_GoodsCoupon, '/goods_coupon', endpoint='goods_coupon')
coupon_api.add_resource(Coupon_UserCoupon, '/user_coupon', endpoint='user_coupon')

