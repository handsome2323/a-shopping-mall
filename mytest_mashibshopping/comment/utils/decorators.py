from flask import g


'''
自定义一个装饰器，用于验证某些请求是否已经登录过了，如果已经登录过了，就继续访问。

本质上是一个登录拦截
'''

def loggin_required(func):
    def wrapper(*args,**kwargs):

        if g.user_id is not None:

            return func(*args,**kwargs)
        else:
            return {'msg':'invalid token'},401

    return wrapper