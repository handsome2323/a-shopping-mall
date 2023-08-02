import json
import time
from flask import g
from flask_restful import Resource, reqparse
from flask_restful.reqparse import RequestParser

from shopping.resource.cart import Shopping_Cart
from comment.models import db
from comment.models.coupon import SmsCoupon, SmsCouponProductCategoryRelation, SmsCouponHistory
from comment.models.goods import SkuStock, ProductFullReduction
from comment.models.order import Order, OrderItem
from comment.models.user import User
from comment.utils.data2dict import datalist2dict, data2dict
from comment.utils.decorators import loggin_required
from comment.utils.gen_trans_id import gen_trans_id


class Shopping_Order_List(Resource):
    """ 订单列表 """
    method_decorators = {
        'get': [loggin_required]
    }

    def get(self):
        rp = RequestParser()

        rp.add_argument('pageIndex', required=True)
        rp.add_argument('pageSize', required=True)
        args = rp.parse_args()
        page = int(args.pageIndex)
        page_size = int(args.pageSize)
        self.user_id = g.user_id
        self.user = User.query.filter(User.id == self.user_id).first()
        # 根据用户id查询订单，筛选订单状态为未删除的
        res = Order.query.filter(Order.user_id == self.user.username, Order.delete_status == 0).order_by(-Order.gmt_create).\
            paginate(page=page, per_page=page_size, error_out=False)
        if res:
            data = {}
            data['has_next'] = res.has_next  # 是否还有下一页
            data['has_prev'] = res.has_prev  # 是否还有上一页
            data['next_num'] = res.next_num  # 下一页的页码
            data['page'] = res.page  # 当前页的页码
            data['pages'] = res.pages  # 匹配的元素在当前配置一共有多少页
            data['totalElements'] = res.total  # 匹配的元素总数
            data['content'] = datalist2dict(res.items)
            return data
        else:
            return {'msg': 'ok', 'code': 200}


class Shopping_Order(Resource):
    """
        购物订单
    """
    method_decorators = {
        'get': [loggin_required],
        'post': [loggin_required],
        'put': [loggin_required],
    }

    def put(self):
        # 订单支付完成
        rp = RequestParser()
        rp.add_argument('orderId', required=True)  # 使用的优惠券集合
        args = rp.parse_args()
        order_id = args.orderId
        order = Order.query.filter(Order.order_number == order_id).first()
        if order:
            order.order_status = 2
            db.session.commit()
            return {'msg': 'finished'}


    def post(self):
        # 创建订单
        rp = RequestParser()
        rp.add_argument('memberReceiveAddressId', required=True)  # 收货地址ID
        rp.add_argument('receiverDetailAddress', required=True)  # 收货详细地址
        rp.add_argument('receiverPhone', required=True)  # 收货人手机
        rp.add_argument('receiverName', required=True)   # 收货人名字
        rp.add_argument('payType', required=True)  # 支付类型
        rp.add_argument('goodsitems', required=True)  # 购买商品合集
        rp.add_argument('useCouponIds', required=True)  # 使用的优惠券集合
        args = rp.parse_args()
        self.adressId = args.memberReceiveAddressId
        self.detailAddress = args.receiverDetailAddress
        self.receiver_phone = args.receiverPhone
        self.receiver_name = args.receiverName
        self.pay_type = args.memberReceiveAddressId
        self.order_goods = json.loads(args.goodsitems)
        self.use_coupon_ids = json.loads(args.useCouponIds)
        self.user_id = g.user_id
        self.user = User.query.filter(User.id == self.user_id).first()
        return self.create_order()

    def get(self):
        # 获取单个订单的详情
        rp = RequestParser()
        rp.add_argument('orderNumber', required=True, type=int)  # 订单号码
        args = rp.parse_args()
        order_number = args.orderNumber
        order_detail_list = []
        res = Order.query.filter(Order.order_number == order_number).first()  # 订单对象
        if res:
            res_data = data2dict(res)
            # 订单详情
            items = OrderItem.query.filter(OrderItem.order_number == order_number).all()
            res_data['items'] = datalist2dict(items)
            return res_data
        else:
            return {'message': 'none'}

    def create_order(self):
        # 创建订单

        self.check_stock()
        if self.order_out_stock:
            return {'message': '不分商品库存不足'}, 400
        else:

            self.order_number = gen_trans_id()  # 生成订单id
            self.create_time = time.time() * 1000  # 创建时间
            user_id = g.user_id  # 获取当前用户id
            # 计算总价
            self.get_order_totalAmount()
            # 计算满减金额
            self.get_goods_discont()
            # 计算优惠券金额
            self.get_coupon_discont()
            try:
                # 扣减库存
                self.set_proSku_num()
                # 设置用户优惠券状态
                self.set_user_coupon()
                # 实付金额
                pay_amount = self.total_amount - float(self.total_discont) - float(self.coupon_discont)
                # 生成订单
                self.shopping_order = Order(user_id=self.user.username, order_number=self.order_number, gmt_create=self.create_time,
                                            receiver_name=self.receiver_name, receiver_phone=self.receiver_phone,
                                            pay_type=self.pay_type, total_amount=self.total_amount, pay_amount=pay_amount,
                                            receiver_detail_address=self.detailAddress, create_by=self.user.username)
                db.session.add(self.shopping_order)
                self.create_order_detatil()  # 生成订单详情
                # 移除购物车商品
                db.session.commit()
                self.remove_cart_goods()
                return {'orderId': self.shopping_order.order_number}
            except Exception as e:
                print(e)
                db.session.rollback()
                return {'message': '服务器忙, 请稍后重试'}, 500

    def remove_cart_goods(self):
        # 移除购物车商品 (生成订单的那些商品)
        Shopping_Cart.set_Shopping_cart('delete', self.order_goods)

    def check_stock(self):
        """ 检查订单库存 """
        self.order_out_stock = False  # 是否库存不足
        for item in self.order_goods:
            sku_no = item['sku_no']  # 库存id
            goods_num = int(item['quantity'])  # 要购买的库存数量
            item_sku = SkuStock.query.filter(SkuStock.sku_no == sku_no).first()  # 获取具体的库存
            if goods_num >= item_sku.num > 0:  # 比较要购买数量和所剩库存
                self.order_out_stock = True

    def get_order_totalAmount(self):
        """ 获取订单总金额 """
        self.total_amount = 0
        for item in self.order_goods:
            sku_no = item['sku_no']
            goods_num = int(item['quantity'])
            item_sku = SkuStock.query.filter(SkuStock.sku_no == sku_no).first()

            goods_amount = item_sku.price * goods_num  # 订单中 单一商品的总价  sku价格 * 购买数量
            item['goods_price'] = item_sku.price  # sku价格
            item['goods_amount'] = goods_amount  # 添加到商品属性中去
            self.total_amount += goods_amount

    def get_goods_discont(self):
        """ 检查商品满减 """
        self.total_discont = 0  # 总的满减优惠金额
        for item in self.order_goods:
            cur_item_proId = int(item['productId'])  # 商品id
            cur_item_discont = ProductFullReduction.query.filter(ProductFullReduction.product_id
                                                                 == cur_item_proId).first()
            # item['sell_price'] 对应 订单详情中的 product_price 销售价格
            if item['goods_price'] >= cur_item_discont.full_price:
                item['sell_price'] = item['goods_price'] - float(cur_item_discont.reduce_price)
            else:
                item['sell_price'] = item['goods_price']

            # 判断 单一商品购买总金额是否满足 商品满减条件
            if item['goods_amount'] >= cur_item_discont.full_price:
                self.total_discont += cur_item_discont.reduce_price
                print(self.total_discont)

    def get_coupon_discont(self):
        """ 获取优惠券折扣 """
        self.coupon_discont = 0  # 总的优惠券 优惠金额
        for coupon_id in self.use_coupon_ids:
            # 根据优惠券id 查询 优惠券对应的3级商品品类id 和 具体的 优惠券对象
            coupon_item = db.session.query(SmsCoupon, SmsCouponProductCategoryRelation.product_category_id).join(
                SmsCouponProductCategoryRelation, SmsCoupon.id == SmsCouponProductCategoryRelation.coupon_id).filter(
                SmsCoupon.id == int(coupon_id)).first()
            coupon_category_id = coupon_item.product_category_id  # 3级品类id
            coupon_min_point = coupon_item.SmsCoupon.min_point  # 优惠券满减条件金额 例 500-50 的 500
            coupon_amount = coupon_item.SmsCoupon.amount  # 优惠券满减金额 例 500-50 的 50
            category_goods_total_amount = 0
            for item in self.order_goods:
                if int(item['categoryId']) == coupon_category_id:  # 当前商品类别是否和优惠券对应商品类别一直
                    category_goods_total_amount += item['goods_amount']  # 一致则累计到 当前商品分类总金额
            if category_goods_total_amount >= coupon_min_point:  # 当前商品分类总金额 是否 满足 优惠券使用条件
                self.coupon_discont += coupon_amount

    def create_order_detatil(self):
        """ 创建订单详情 """
        order_detail_list = []
        for item in self.order_goods:
            sku_no = item['sku_no']
            sku_item = SkuStock.query.filter(SkuStock.sku_no == sku_no).first()
            order_id = self.shopping_order.id
            order_number = self.shopping_order.order_number
            pro_id = sku_item.rel_product_id
            pro_pic = sku_item.image
            pro_name = sku_item.title
            pro_categoryId = int(item['categoryId'])
            pro_spec = sku_item.spec
            price = sku_item.price
            quantity = item['quantity']
            product_price = item['sell_price']
            order_item = OrderItem(order_id=order_id, order_number=order_number, product_id=pro_id, product_pic=pro_pic,
                                   product_name=pro_name, product_category_id=pro_categoryId, product_attr=pro_spec,
                                   gmt_create=self.create_time, create_by=self.user.username, product_normal_price=price,
                                   product_price=product_price, product_settlement_price=price, product_quantity=quantity,
                                   product_spu_id=sku_item.rel_product_id)
            db.session.add(order_item)

    def set_proSku_num(self):
        """ 设置商品库存 """
        for item in self.order_goods:
            sku_no = item['sku_no']
            goods_num = int(item['quantity'])
            item_sku = SkuStock.query.filter(SkuStock.sku_no == sku_no).first()
            print(item_sku.id)
            item_sku.num -= goods_num

    def set_user_coupon(self):
        """ 更改用户优惠券使用状态 """
        for coupon_id in self.use_coupon_ids:
            coupon_history = SmsCouponHistory.query.filter(SmsCouponHistory.coupon_id == coupon_id, SmsCouponHistory.
                                                           member_id == self.user_id).first()
            coupon_history.use_status = 1
