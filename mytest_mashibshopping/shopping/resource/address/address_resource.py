#coding: utf8

from flask import g, request
from flask_restful import Resource, reqparse
from flask_restful.reqparse import RequestParser
from comment.utils.data2dict import datalist2dict, data2dict

from comment.models import db
from comment.models.address import Address
from comment.models.user import User
print("导入地址类")

class User_Address(Resource):
    """
        用户地址管理
    """

    # 查询用户地址列表
    def get(self):
        rp = RequestParser()
        rp.add_argument('username', required=True)
        args = rp.parse_args()
        username = args.username

        res = Address.query.join(User, Address.login_user == User.username).\
            filter(Address.login_user == username, Address.enabled == 1).all()

        res_data = datalist2dict(res)

        if res:
            return res_data
        else:
            return {'msg': '', 'code': 201}

    # 新增用户地址
    def post(self):
        rp = RequestParser()
        rp.add_argument('address', required=True)
        rp.add_argument('area', required=True)
        rp.add_argument('city', required=True)
        rp.add_argument('defaultAddress', required=True)
        rp.add_argument('loginUser', required=True)
        rp.add_argument('province', required=True)
        rp.add_argument('recipient', required=True)
        rp.add_argument('telephone', required=True)
        args = rp.parse_args()
        address = args.address
        area = args.area
        city = args.city
        defaultAddress = 1 if args.defaultAddress == 'true' else 0
        loginUser = args.loginUser
        province = args.province
        recipient = args.recipient
        telephone = args.telephone

        if defaultAddress:
            self.set_default_false(loginUser)

        add = Address(login_user=loginUser, recipient=recipient, address=address, area=area, city=city, default_address=
                      defaultAddress, province=province, telephone=telephone, enabled=1)
        db.session.add(add)
        db.session.commit()
        return {'msg': 'ok', 'code': 200}


    # 更新用户地址
    def put(self):
        rp = RequestParser()
        rp.add_argument('address', required=True)
        rp.add_argument('area', required=True)
        rp.add_argument('city', required=True)
        rp.add_argument('id', required=True)
        rp.add_argument('defaultAddress', required=True)
        rp.add_argument('loginUser', required=True)
        rp.add_argument('province', required=True)
        rp.add_argument('recipient', required=True)
        rp.add_argument('telephone', required=True)
        args = rp.parse_args()
        address = args.address
        area = args.area
        city = args.city
        add_id = args.id
        defaultAddress = 1 if args.defaultAddress == 'true' else 0
        loginUser = args.loginUser
        province = args.province
        recipient = args.recipient
        telephone = args.telephone

        if defaultAddress:
            self.set_default_false(loginUser)

        res = Address.query.filter(Address.login_user == loginUser, Address.id == add_id)
        if res:
            res.update({'address': address, 'area': area, 'city': city, 'default_address': defaultAddress,
                        'login_user': loginUser, 'province': province, 'recipient': recipient, 'telephone': telephone, })
        db.session.commit()
        return {'msg': 'ok', 'code': 200}

    # 删除用户地址
    def delete(self):
        rp = RequestParser()
        rp.add_argument('id', required=True)
        args = rp.parse_args()
        id = args.id
        res = Address.query.filter(Address.id == id).first()
        if res:
            res.enabled = 0
            db.session.commit()
            return {'msg': 'delete finish', 'code': 200}

    def set_default_false(self, username):
        res = Address.query.filter(Address.default_address == 1, Address.login_user == username)
        if res:
            res.first().default_address = 0
            db.session.commit()







