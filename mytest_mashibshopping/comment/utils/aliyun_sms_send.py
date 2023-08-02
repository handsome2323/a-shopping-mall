# # -*- coding: utf-8 -*-
# import sys
# from comment.utils.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
# from comment.utils.aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
# from aliyunsdkcore.client import AcsClient
# import uuid
# from aliyunsdkcore.profile import region_provider
# from aliyunsdkcore.http import method_type as MT
# from aliyunsdkcore.http import format_type as FT
# from comment.utils import const
#
# """
# 短信业务调用接口示例，版本号：v20170525
#
# Created on 2017-06-12
#
# """
#
# # 注意：不要更改
# REGION = "cn-shanghai"
# SIGN_NAME='马士兵老师'
# TEMPLATE_id='SMS_193519304'
# acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
#
# '''
# phone_numbers :发送短信的目标手机号码
# sign_name ： 短信的签名
# template_code ： 申请成功之后模板ID
# '''
# def send_sms(phone_numbers, code):
#     business_id = uuid.uuid1()  # 通过UUID生成一个随机的ID
#
#     smsRequest = SendSmsRequest.SendSmsRequest()
#     # 申请的短信模板编码,必填
#     smsRequest.set_TemplateCode(TEMPLATE_id)
#
#     # 短信模板变量参数
#     if code is not None:
#         params = "{\"code\":\""+code+"\"}"  # 发送的手机验证码
#         smsRequest.set_TemplateParam(params)
#
#     # 设置业务请求流水号，必填。
#     smsRequest.set_OutId(business_id)
#
#     # 短信签名
#     smsRequest.set_SignName(SIGN_NAME)
#
#     # 数据提交方式
#     # smsRequest.set_method(MT.POST)
#
# 	# 数据提交格式
#     # smsRequest.set_accept_format(FT.JSON)
#
#     # 短信发送的号码列表，必填。
#     smsRequest.set_PhoneNumbers(phone_numbers)
#
#     # 调用短信发送接口，返回json
#     smsResponse = acs_client.do_action_with_exception(smsRequest)
#
#     # TODO 业务处理
#
#     return smsResponse.decode('utf-8')
#
#
#
# if __name__ == '__main__':
#     result = send_sms("13229452942", '123453')
#     print(result)
#
#
#
#
#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential

credentials = AccessKeyCredential('<your-access-key-id>', '<your-access-key-secret>')
# use STS Token
# credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')
client = AcsClient(region_id='cn-hangzhou', credential=credentials)

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2017-05-25')
request.set_action_name('SendSms')

response = client.do_action(request)
# python2:  print(response)
print(str(response, encoding = 'utf-8'))