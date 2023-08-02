# 代表用户模块下的蓝图，包括用户模块下的所有资源
from flask import Blueprint
#创建资源的api对象
from flask_restful import Api
from comment.utils.output import output_json

user_bp=Blueprint('users',__name__,url_prefix='/user')
user_api=Api(user_bp) #创建资源api



#使用我们自定义的json,替换装饰器的写法
user_api.representation('application/json')(output_json)



#加载当前模块的资源
from shopping.resource.user.user_resource import shopping_user, user_sms,AuthorizationCodeResource,RegisterUserResource,\
    user_loggin_Resource,IsExits_phone_Resource,user_logginout_Resource

user_api.add_resource(shopping_user,'/hello')

#加载验证码资源
user_api.add_resource(user_sms,'/sms')

#加载验证手机和验证码
user_api.add_resource(AuthorizationCodeResource,'/authorization')

#加载用户注册信息
user_api.add_resource(RegisterUserResource,'/register')

#加载用户登录信息
user_api.add_resource(user_loggin_Resource,'/login')

#  添加请求钩子
# from comment.utils.request_wares import jwt_request_authorization
#
# user_api.before_request(jwt_request_authorization,'/')  # 所有服务器的请求都有当前的请求钩子

# 判断手机号码是否存在
user_api.add_resource(IsExits_phone_Resource,'/isExist')


#退出登录

user_api.add_resource(user_logginout_Resource,'/loginOut')