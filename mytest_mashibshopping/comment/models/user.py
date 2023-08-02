
from comment.models import db

from datetime import datetime

from werkzeug.security import generate_password_hash,check_password_hash

#用户的模型类
class User(db.Model):
    __tablename__ = 't_user'
    id=db.Column(db.BIGINT,primary_key=True,autoincrement=True)
    username = db.Column(db.String(64), doc='用户名')
    # 数据库表中存放的是 加密之后的密文，采用flask提供的hash算法:生成一个128位密文
    password = db.Column(db.String(128), doc='密码')
    icon = db.Column(db.String(5000), doc='用户头像图片')
    email = db.Column(db.String(100), doc='邮箱')
    nick_name = db.Column(db.String(200), doc='昵称')
    note = db.Column(db.String(500), doc='备注')
    phone = db.Column(db.String(11), doc='手机号')
    #时间信息


    login_date=db.Column(db.DateTime,default=datetime.now(),doc='用户登录时间')
    create_time=db.Column(db.DateTime,default=datetime.now(),doc='用户注册时间')
    update_time=db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now(),doc='用户修改时间')
    status=db.Column(db.Integer,doc='用户状态')



    #是一个pwd属性的getter函数
    @property
    def pwd(self):
        return self.password


    #是一个pwd属性的getter函数
    @pwd.setter
    def pwd(self,x_password):
        '''
        根据明文的密码，转成密文
        :param x_password:
        :return:
        '''
        self.password=generate_password_hash(x_password) #根据flask框架提供的算法进行加密



    def check_pwd(self,x_password):



        return check_password_hash(self.password,x_password)