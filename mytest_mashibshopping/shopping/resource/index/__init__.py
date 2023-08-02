#代表商品分类模块下的蓝图，包括商品分类资源
from flask import Blueprint
#创建资源的api对象

from flask_restful import Api

from comment.utils.output import output_json

index_bp=Blueprint('index',__name__,url_prefix='/index')

index_api=Api(index_bp) #创建资源api

index_api.representation('application/json')(output_json)

from shopping.resource.index.index_resource import *

#加载我们的商品分类蓝图

index_api.add_resource(Shopping_Category,'/category')
#测试字典转换资源
# index_api.add_resource(,'/Dict_test')

#获取新品推荐
index_api.add_resource(Shopping_HomeNewProduct,'/home_new_product')
#获取人气热搜
index_api.add_resource(Shopping_HomeRecommendProduct,'/home_recommend_product')

#获取专题资源
index_api.add_resource(Shopping_RecommendSubject,'/recommend_subject')