from flask_restful import Resource

from comment.models.user import User

from flask import current_app, request,g

import random

import json


from comment.utils.lexuntong_sms_send import send_sm

from comment.utils.limiter import limiter as lmt

from flask_limiter.util import get_remote_address

from comment.utils.shopping_redis import redis_client

from comment.utils.token_jwt import generate_tokens,verify_tokens

from shopping.resource.user import constants

from flask_restful.reqparse import RequestParser

from comment.models import db

from comment.utils import parser


from comment.utils.decorators import loggin_required

print("导入用户类")
# 我们定义的资源类
class shopping_user(Resource):
    # 定义限流的速率，三个参数 参数1限流的速率 参数key_func 参数3限流的提示信息

    error_message = 'too many requests'
    # decorators = [
    #     lmt.limit(constants.LIMTT_SMS_COOE_BY_MOBILE,
    #               key_func=lambda: request.args.get(['phone']),
    #               error_message=error_message
    #               ),
    #     lmt.limit(constants.LIMTT_SMS_COOE_BY_IP,
    #               key_func=get_remote_address,
    #               error_message=error_message
    #               )
    #
    # ]

    '''
    在get的函数上加上登录的拦截，
    '''

    # method_decorators = {
    #     'get': [loggin_required],
    #     'post': [loggin_required],
    #     'put': [loggin_required]
    #
    # }

    def get(self):
        print('执行get请求')
        current_app.logger.debug('get请求')
        current_app.logger.info('我得测试日志')
        return {
            'hello': '测试'
        }

    def post(self):
        return {

            'hello': 'post测试'

        }


class user_sms(Resource):

    def get(self):
        phone = request.args.get('phone').strip()
        p = User.query.filter(User.phone == phone).first()
        #检查手机号是否唯一
        if p:
            current_app.logger.info('{}:用户名已经存在,请再换一个'.format(phone))
            return {'message': 'the phone is already exits'}, 400

        code = random.randint(1000, 9999)
        # code=lexuntong_sms_send.param
        a = send_sm(phone=phone, code=str(code))
        print('验证码',code)
        redis_client.setex('shopping:code{}'.format(phone),
                           constants.SMS_CDDE_EXPRIRES, code)  # 参数1 是key值 ，参数2是时效性

        return {'smscode':code}


# print(kobgine.base.Engine ROLLBACK
# 127.0.0.1 - - [22/Nov/2021 19:29:54] "GET /goods/merchant_hotsales?merchant_id=1 HTTP/1.1" 200 -
# 127.0.0.1 - - [22/Nov/2021 19:29:58] "POST /cart/user_cart HTTP/1.1" 401 -
# 获取的token的值为---> None
# 解密后的result为---> {'message': 'token 验证失败'}
# 获取的token的值为---> None
# 解密后的result为---> {'message': 'token 验证失败'}
#  * Detected change in 'D:\\xiaolin_repo\\xiaolin_repo\\mytest_mashibshopping\\shopping\\resource\\goods\\goods_resource.py', reloading
#  * Restarting with stat
# 导入用户类
# 导入地址类
#  * Debugger is active!
#  * Debugger PIN: 183-491-758e().get())
# text_rece = urllib.request.urlopen(request).read().decode('utf-8')
# result=send_sms(phone_number,str(code))
# result=json.loads(result)
#
# result['phone']=phone_number

# code=text_rece[]


# 短信发送成功后，还需要把验证码放到redis数据库中，以便于下次验证，验证码的时效为五分钟
# redis_client.setex('shopping:code{}'.format(phone_number),
#                    constants.SMS_CDDE_EXPRIRES,code)  #参数1 是key值 ，参数2是时效性



# return result


#
# a=send_sm('13229452942','6543')
# print(a)

class AuthorizationCodeResource(Resource):
    '''

    提交手机号和验证码，验证

    '''

    def post(self):
        rp = RequestParser()

        rp.add_argument('phone', type=parser.mobile, required=True)

        rp.add_argument('code', type=parser.regex(r'^\d{4}$'), required=True)

        args = rp.parse_args()
        # print(args)
        phone = args.phone

        code = args.code

        # 从redis数据中 得到之前保存的验证码

        key = 'shopping:code{}'.format(phone)

        try:
            real_code = redis_client.get(key)

        except ConnectionError as e:
            current_app.logger.error(e)

            return {'message': 'redis connect error '}, 400

        # 开始校验
        if not real_code or real_code.decode() != code:
            return {'message': 'Invalid code'}, 400

        return {'phone': phone, 'msg': 'ok'}


class RegisterUserResource(Resource):
    '''

    #完成用户的注册，填写账号信息

    '''

    def post(self):
        rp = RequestParser()

        rp.add_argument('phone', type=parser.mobile, required=True)

        # rp.add_argument('code', type=parser.regex(r'^\d{5}$'), required=True)

        rp.add_argument('username', required=True)

        rp.add_argument('password', required=True)

        rp.add_argument('email', type=parser.email, required=True)

        args = rp.parse_args()

        username = args.username

        password = args.password

        phone = args.phone

        email = args.email
        # 验证用户名是否唯一 :先从mysql数据库中根据当前用户名查询
        u = User.query.filter(User.username == username).first()
        if u:  # 用户名已经存在
            current_app.logger.info('{}:用户名已经存在,请再换一个'.format(username))
            return {'message': 'the username is already exits'}, 400
        #验证邮箱是否唯一 :先从mysql数据库中根据当前用户名查询
        email=User.query.filter(User.email == email).first()
        if email:
            current_app.logger.info('{}:用户名已经存在,请再换一个'.format(email))
            return {'message': 'the email is already exits'}, 400

        user = User(username=username, pwd=password, email=email, phone=phone,status=0)

        db.session.add(user)

        db.session.commit()

        return {'msg': 'ok'}


class user_loggin_Resource(Resource):
    '''

    登录

    '''

    def post(self):

        username = request.form.get('username')

        password = request.form.get('password')

        if not all([username, password]):
            return {'massage': 'data is not all'}, 402

        user = User.query.filter(User.username == username).first()

        if user:
            if user.check_pwd(password):

                #创建token
                token = generate_tokens(user.id)
                print('这个是token值>>>>>>>>>>',token)
                return {'msg': 'login is success', 'token': token,'username':username}

        return {'message': 'user is error or password error'},402


class user_logginout_Resource(Resource):
    '''
    退出登录

    '''
    def post(self):
        if g.user_id:

            g.user_id=None

        return {'msg':'退出登录'}




class IsExits_phone_Resource(Resource):


    '''

    判断手机号是否存在

    '''
    def post(self):

        phone_number=request.form.get('phone')
        print('这个是手机号码',phone_number)

        user=User.query.filter(User.phone==phone_number).first()
        db.session.drop()
        if user: #如果用户有，则代表手机已存在

            return {'isExist':True,'message':'此手机号码已经注册','code':201}

        return {'msg':'手机号可以注册'}





