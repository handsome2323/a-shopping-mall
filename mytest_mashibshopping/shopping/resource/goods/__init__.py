from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

goods_bp = Blueprint('goods', __name__, url_prefix='/goods')  # 创建蓝图
goods_api = Api(goods_bp)  # 创建蓝图中的资源API

# 使用我们自定义json格式，替代装饰器的写法
goods_api.representation('application/json')(output_json)

from shopping.resource.goods.goods_resource import *

goods_api.add_resource(Goods_GoodsList, '/goods_list', endpoint='goods_list')
goods_api.add_resource(Goods_GoodsSpecification, '/goods_specification', endpoint='goods_specification')
goods_api.add_resource(Goods_GoodsDetail, '/good_detail', endpoint='goods_detail')
goods_api.add_resource(Goods_GoodsFullReduction, '/good_fullReduction', endpoint='good_fullReduction')
goods_api.add_resource(Goods_MerchantHotsales, '/merchant_hotsales', endpoint='merchant_hotsales')
goods_api.add_resource(Goods_GoodSkuDetail, '/good_sku_detail', endpoint='good_sku_detail')
goods_api.add_resource(Goods_CartSkuDetail, '/goods_cart_sku_detail', endpoint='goods_cart_sku_detail')
goods_api.add_resource(Goods_Recommend, '/goods_cart_recommend', endpoint='goods_cart_recommend')
