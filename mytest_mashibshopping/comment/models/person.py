from comment.models import db

from datetime import datetime

#用户的模型类
class Person(db.Model):
    __tablename__ = 'person'
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