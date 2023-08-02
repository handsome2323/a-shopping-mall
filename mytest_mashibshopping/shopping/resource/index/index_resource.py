# from flask_restful import Resource,reqparse,request
#
# from comment.models.index import *
#
# from flask import current_app, request,g
#
# import random
#
# from comment.models.goods import Product
#
# import json
# from comment.utils.data2dict import datalist2dict,data2dict
#
# #导入redis数据库
# from comment.utils.shopping_redis import redis_client
#
# # 商品资源分类
# class shopp_category(Resource):
#
#     def get(self):
#         #从redis数据库读取数据
#         data_search=redis_client.get('index_category')
#         if data_search:
#             return json.loads(data_search)
#
#         else:
#             #如果redis没有数据，则从mysql查询数据，返回给用户，并且写入给redis
#             # rq = reqparse.RequestParser()
#             # rq.add_argument('parent_id', required=True, type=int)
#             # req = rq.parse_args()
#             data = self.get_data(0)
#             if data:
#
#                 for item in data:
#                     item.update({'list':''})
#
#                     secend_data=self.get_data(item['id'])
#
#                     for item1 in secend_data:
#
#                         item1.update({'list':''})
#
#                         third_data=self.get_data(item1['id'])
#
#                         item1['list']=third_data
#
#
#                 redis_client.setex('index_category',3600*24,json.dumps(data))
#
#                 print(data)
#                 return data
#             else:
#
#                 return {'message':'none'}
#
#     @staticmethod
#     def get_data(parent_id):
#         res = category.query.with_entities(category.id, category.parent_id, category.name) \
#             .filter(category.parent_id == parent_id).order_by(category.sort.asc()).limit(10).all()
#
#         if res:
#
#             return datalist2dict(res)
#
#         else:
#             return 'none'
#
# # 测试资源
# class Dict_test(Resource):
#     def get(self):
#
#     #取多条数据，多条字段
#         res=category.query.with_entities(category.id,category.name).filter(category.parent_id==0).all()
#         if res:
#
#             return datalist2dict(res)
#         else:
#
#             return {'message':'none'}
#
#
#
#
# #商品资源类
#
# class shopping_home_new_product(Resource):
#     def get(self):
#         res=HomeNewProduct.query.join(Product,HomeNewProduct.product_id==Product.id)\
#             .with_entities(Product.id,Product.default_pic,Product.price,Product.product_name,
#                            Product.rel_category3_id).order_by(HomeNewProduct.sort.asc())\
#             .limit(10).all()
#         if res:
#             return datalist2dict(res)
#
#         else:
#             return {'message':'none'}
#
#
# #首页人气热搜的资源类
# class shopping_homerecommend_product(Resource):
#
#     def get(self):
#
#         data_cathe=redis_client.get('index_homerecommend_product')
#
#         if data_cathe:
#             return json.loads(data_cathe)
#
#         else:
#             res=HOMERecommendproduct.query.join(Product,HOMERecommendproduct.product_id==Product.id) \
#                 .with_entities(Product.id, Product.default_pic,Product.price ,Product.product_name,
#                                Product.rel_category3_id)\
#                 .limit(10).all()
#             if res:
#                 data=datalist2dict(res)
#                 redis_client.setex('index_homerecommend_product',3600*24,json.dumps(data))
#                 return data
#             else:
#                 return {'message':'none'}
#
#
#
# class shopping_rocommendsubject(Resource):
#     def get(self):
#         data_cathe = redis_client.get('index_HomeRecommendProduct')
#
#         if data_cathe:
#             return json.loads(data_cathe)
#
#         else: # redis中没有数据，则查询mysql数据库，把查询结果写入到redis,并返回数据
#             res = HOMERecommendproduct.query.join(Product,
#                              HOMERecommendproduct.product_id == Product.id).with_entities \
#                 (Product.id, Product.default_pic, Product.price, Product.product_name,
#                  Product.rel_category3_id).limit(
#                 10).all()
#             if res:
#                 data = datalist2dict(res)
#
#                 # 将查询数据写入redis
#                 redis_client.setex("index_HomeRecommendProduct", 3600 * 24, json.dumps(data))
#
#                 return data
#             else:
#                 return {'message': 'none'}
#
# # #首页专题资源类
# class Shopping_RecommendSubject(Resource):
#     def get(self):
#         res = CmsSubject.query.filter(
#             CmsSubject.show_status == 1).all()
#
#         res_list = []
#         for res_obj in res:
#             if res_obj:
#                 data = data2dict(res_obj)
#                 res_product = CmsSubjectProductRelation.query.join \
#                     (Product, CmsSubjectProductRelation.product_id == Product.id).filter \
#                     (CmsSubjectProductRelation.subject_id == res_obj.id).with_entities \
#                     (Product.id, Product.default_pic, Product.price, Product.product_name,
#                      Product.rel_category3_id).limit(10).all()
#                 if res_product:
#                     data_product = datalist2dict(res_product)
#                     data['productList'] = data_product
#                     res_list.append(data)
#         print(res_list)
#         if len(res_list) > 0:
#             return res_list
#         else:
#             return {'message': 'none'}
#
#
#
import json

from flask_restful import Resource, reqparse, request
from flask import current_app
from comment.models.goods import Product, Specification, SpecificationOption, ProductFullReduction, SkuStock
from comment.utils.data2dict import datalist2dict, data2dict
# from comment.models.index import *
from comment.utils.shopping_redis import redis_client
from comment.models.index import HOMERecommendproduct, HomeNewProduct, category, CmsSubject, \
    CmsSubjectCategory, CmsSubjectProductRelation


# 商品分类的资源类
class Shopping_Category(Resource):

    def get(self):
        # 从redis读取数据
        data_cache = redis_client.get("index_category")
        if data_cache:  # 如果redis中有数据，则返回redis中的数据
            return json.loads(data_cache)
        else:  # redis中没有数据，则查询mysql数据库，把查询结果写入到redis,并返回数据
            data = self.getData(0)
            if data:
                for item in data:
                    item.update({'list': ''})
                    data_second = self.getData(int(item['id']))
                    item['list'] = data_second
                    for item1 in data_second:
                        item1.update({'list': ''})
                        data_third = self.getData(int(item1['id']))
                        item1['list'] = data_third
                # 将查询数据写入redis
                redis_client.setex("index_category", 3600 * 24, json.dumps(data))
                return data
            else:
                return {'message': 'none'}

    # 获取分类数据的静态方法
    @staticmethod
    def getData(parent_id):
        res = category.query.with_entities(category.id, category.parent_id, category.name).filter(
            category.parent_id == parent_id).order_by(category.sort.asc()).limit(10).all()


        print('这是res',res)
        if res:
            return datalist2dict(res)
        else:
            return 'none'


# 首页
class Shopping_HomeNewProduct(Resource):
    def get(self):
        try:
            # res = HomeNewProduct.query.limit(10).all()
            res = HomeNewProduct.query.join(Product, HomeNewProduct.product_id == Product.id).with_entities \
                (Product.id, Product.default_pic, Product.price, Product.product_name,
                 Product.rel_category3_id).limit(10).all()
            # res = HomeNewProduct.query.filter(HomeNewProduct.id==16).first()
            print('mysql中获取的res--->', res)

            if res:
                data = datalist2dict(res)
                return data
        # else:
        except Exception as e:
            current_app.logger.error(e)
            print('error------>', e)
            # raise
            return {'message': 'none'}
    def post(self):
        pass

# 首页人气热搜的资源类
class Shopping_HomeRecommendProduct(Resource):
    def get(self):
        # 从redis读取数据
        data_cache = redis_client.get("index_HomeRecommendProduct")
        if data_cache:  # 如果redis中有数据，则返回redis中的数据
            return json.loads(data_cache)
        else:  # redis中没有数据，则查询mysql数据库，把查询结果写入到redis,并返回数据
            res = HOMERecommendproduct.query.join(Product,
                                                  HOMERecommendproduct.product_id == Product.id).with_entities \
                (Product.id, Product.default_pic, Product.price, Product.product_name,
                 Product.rel_category3_id).limit(
                10).all()
            print(str(res))
            # print('mysql中的res--->', res)
            if res:
                data = datalist2dict(res)
                print('-----------------------', data)
                # 将查询数据写入redis
                redis_client.setex("index_HomeRecommendProduct", 3600 * 24, json.dumps(data))
                return data
            else:
                return {'message': 'none'}


class Shopping_RecommendSubject(Resource):
    def get(self):
        res = CmsSubject.query.filter(
            CmsSubject.show_status == 1).all()

        res_list = []
        for res_obj in res:
            if res_obj:
                data = data2dict(res_obj)
                res_product = CmsSubjectProductRelation.query.join \
                    (Product, CmsSubjectProductRelation.product_id == Product.id).filter \
                    (CmsSubjectProductRelation.subject_id == res_obj.id).with_entities \
                    (Product.id, Product.default_pic, Product.price, Product.product_name,
                     Product.rel_category3_id).limit(10).all()
                if res_product:
                    data_product = datalist2dict(res_product)
                    data['productList'] = data_product
                    res_list.append(data)
        if len(res_list) > 0:
            return res_list
        else:
            return {'message': 'none'}
