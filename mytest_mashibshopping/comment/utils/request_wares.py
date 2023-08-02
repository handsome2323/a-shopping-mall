
from flask import g,request,current_app
from comment.utils.token_jwt import verify_tokens
'''

定义请求钩子，请求进来之前得到request携带的token,并且验证token
'''


def jwt_request_authorization():
    '''

    自定义请求钩子参数，验证token,并把请求验证成功之后的用户id保存到全局变量g中
    :return:
    '''

    g.user_id = None #定义一个全局变量 user_id

    try:
        token =request.headers.get('token')
        print('获取的token的值为--->', token)

    except Exception as e:

        current_app.logger.info('没有 token ')
        return
    result=verify_tokens(token)
    print('解密后的result为--->', result)

    if 'id' in result:  #如果验证成功，那么字典中一定有用户id
        # print()
        g.user_id=result['id']

