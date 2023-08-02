from flask import Flask
from setting import map_config
from flask import current_app
#负责创建app对象的
def creat_app(config_type):
    app=Flask(__name__)
    #加载项目的配置

    app.config.from_object(map_config.get(config_type))
    #初始化限流器
    from comment.utils.limiter import limiter

    limiter.init_app(app)


    #加载日志处理工具
    from comment.utils.logging import creat_app

    creat_app(app)

    #初始化redis数据库

    from comment.utils.shopping_redis import redis_client
    redis_client.init_app(app)

    #添加请求钩子生效
    from comment.utils.request_wares import jwt_request_authorization

    app.before_request(jwt_request_authorization) #所有服务器的请求都生效

    #初始化salaichemy
    from comment.models import db

    # 添加请求钩子
    from comment.utils.request_wares import jwt_request_authorization
    app.before_request(jwt_request_authorization)  # 所有服务器的请求都有当前的请求钩子

    db.init_app(app)
    # 加载user的模块蓝图
    from shopping.resource.user import user_bp

    app.register_blueprint(user_bp)

    #加载商品分类的蓝图
    from shopping.resource.index import index_bp

    app.register_blueprint(index_bp)

    # 加载地址类的蓝图
    from shopping.resource.address import address_bp

    app.register_blueprint(address_bp)

    # 加载coupon分类的蓝图
    from shopping.resource.coupon import coupon_bp

    app.register_blueprint(coupon_bp)
    #加载商品列表蓝图
    from shopping.resource.goods import goods_bp
    app.register_blueprint(goods_bp)
    #加载购物车蓝图
    from shopping.resource.cart import cart_bp
    app.register_blueprint(cart_bp)
    return app

