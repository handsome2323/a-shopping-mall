#代表订单模块下的蓝图，包括订单模块的资源
from flask import Blueprint
#创建资源的api对象
from flask_restful import Api
from comment.utils.output import output_json

order_bp=Blueprint('order',__name__,url_prefix='/order')
order_api=Api(order_bp) #创建资源api



#使用我们自定义的json,替换装饰器的写法
order_api.representation('application/json')(output_json)

from shopping.resource.order.order_resource import *

order_api.add_resource(Shopping_Order, '/shopping_order', endpoint='shopping_order')
order_api.add_resource(Shopping_Order_List, '/shopping_order_list', endpoint='shopping_order_list')
