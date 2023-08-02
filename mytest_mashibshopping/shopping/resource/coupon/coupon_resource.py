import time
from flask import g
from flask_restful import Resource, reqparse
from comment.models.coupon import SmsCoupon, SmsCouponProductCategoryRelation, SmsCouponHistory, \
    SmsCouponProductRelation
from comment.utils.data2dict import datalist2dict, data2dict
from comment.models.index import *
from comment.utils.decorators import loggin_required


class Coupon_GoodsCoupon(Resource):
    """
        商品优惠券
    """

    # 查询商品优惠券列表
    def get(self):
        rp = reqparse.RequestParser()
        rp.add_argument('productCategoryId', required=True, type=int)
        rp.add_argument('spuId', required=True, type=int)
        req = rp.parse_args()
        self.pruduct_id = req.spuId
        self.product_categoryId = req.productCategoryId

        coupon_res = SmsCouponProductCategoryRelation. \
            query.filter(SmsCouponProductCategoryRelation.product_category_id == self.product_categoryId).with_entities(
            SmsCouponProductCategoryRelation.coupon_id).all()
        coupon_list = []
        if coupon_res:
            for item in coupon_res:
                coupon = SmsCoupon.query.filter(SmsCoupon.id == item.coupon_id).first()
                coupon_dict = data2dict(coupon)
                coupon_list.append(coupon_dict)
            return coupon_list
        else:
            return {'message': 'none'}


class Coupon_UserCoupon(Resource):
    """
        用户优惠券
    """
    method_decorators = {
        # 'get': [login_required],
        'post': [loggin_required]
    }

    def post(self):
        rp = reqparse.RequestParser()
        rp.add_argument('couponId', required=True, type=int)
        req = rp.parse_args()
        self.couponId = req.couponId
        user_id = g.user_id

        res = SmsCouponHistory.query.filter(SmsCouponHistory.member_id == user_id, SmsCouponHistory.coupon_id ==
                                            self.couponId).first()
        if res:
            return {'message': '已领取此优惠券', 'code': 201}
        else:
            create_time = int(time.time() * 1000)
            coupon = SmsCouponHistory(coupon_id=self.couponId, member_id=user_id, use_status=0, get_type=1,
                                      create_time=create_time)
            db.session.add(coupon)
            db.session.commit()
            return {'msg': 'ok', 'code': 200}
            # return {'message': '领取成功', 'code': 200}

    def get(self):
        rp = reqparse.RequestParser()
        rp.add_argument('productCategoryIdsS', type=str)
        req = rp.parse_args()
        self.CategoryIdsS = req.productCategoryIdsS
        user_id = g.user_id
        data_list = []
        if self.CategoryIdsS:
            # 订单确认页面的优惠券，只有结算商品对应类目的优惠券
            id_list = self.CategoryIdsS.split(',')
            for id in id_list:
                res = db.session.query(SmsCoupon).join(SmsCouponHistory, SmsCoupon.id == SmsCouponHistory.coupon_id).\
                    join(SmsCouponProductCategoryRelation, SmsCoupon.id == SmsCouponProductCategoryRelation.coupon_id).\
                    filter(SmsCouponHistory.member_id == user_id, SmsCouponProductCategoryRelation.product_category_id
                           == id, SmsCouponHistory.use_status == 0).all()
                if res:
                    res_data = {}
                    res_data['coupons'] = datalist2dict(res)
                    res_data['productCategoryId'] = self.CategoryIdsS
                    data_list.append(res_data)
            return data_list


        else:
            # 个人信息 我的优惠券 用户的所有优惠券
            res = SmsCoupon.query.join(SmsCouponHistory, SmsCoupon.id == SmsCouponHistory.coupon_id).filter \
                (SmsCouponHistory.member_id == user_id, SmsCouponHistory.use_status == 0).with_entities\
                (SmsCoupon.type, SmsCoupon.amount, SmsCoupon.min_point, SmsCoupon.name, SmsCoupon.note,
                 SmsCoupon.start_time, SmsCoupon.end_time, SmsCouponHistory.coupon_id).all()

            if res:
                data = datalist2dict(res)
                return data
            else:
                return {'msg': '无优惠券', 'code': 201}
