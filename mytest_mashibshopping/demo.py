# import time
#
# def deco(func):
#     def wrapper(*args, **kwargs):
#         startTime = time.time()
#         a=1+args[0]
#         return func(*args,**kwargs)
#         # endTime = time.time()
#         # msecs = (endTime - startTime)*1000
#         # print("time is %d ms" %msecs)
#     return wrapper
#
#
# @deco
# def func(a,b):
#     print("hello，here is a func for add :")
#     print("result is %d" %(a))
#
# func(1,b=2)

# class User:
#     """用户模型"""
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def __str__(self):
#         return self.name


# 1. 写装饰器
# def filter_age(func):
#     # 2. 写装饰函数，会覆盖原有的函数
#     def wrapper(*args, **kwargs):
#         # 未满 18 岁不准看电影
#         print(args)
#         print(kwargs['user'])
#         if kwargs['user'].age >= 18:
#             result = func(*args, **kwargs)
#             return result
#         else:
#             # 主动抛出一个错误
#             name = kwargs['user'].name
#             raise Exception(f'{name} 未满18岁不能观看')
#
#     # 3. 在装饰器里面返回装饰函数
#     return wrapper
#
#
# @filter_age
# def watch_movie(user=None):
#     print("%s 正在观看电影" % user)
#
#
# user1 = User('张三', 17)
# user2 = User('李四', 19)
# try:
#     watch_movie(user=user1)
# except Exception as e:
#     print(e)
# watch_movie(user=user2)


# def outer(func):
#     def inner(*args, **kwargs):
#         print(args)
#         print(kwargs)
#         print("偶数和：", sum([i for i in args if i % 2 == 0]))
#         print("奇数和：", sum([i for i in args if i % 2 != 0]))
#         print("偶数和：", sum([i for i in kwargs.values() if i % 2 == 0]))
#         print("奇数和：", sum([i for i in kwargs.values() if i % 2 != 0]))
#
#     return inner
#
#
# @outer
# def func(*args, **kwargs):
#     print(args,kwargs)
#
#
# func(1, 2, 3, 4, a=1, b=2, c=3, d=4)

# b='123'
# a=1
# c=[a,'222']
# if a and b in c:
#     print('111111')
#     print(c)

# b=[1,23,6]
# a=list(map(lambda x:x**2,b))
# print(a)
# print(type(a))
# x,y=2,2

# a=(lambda x,y:x**y,1,2,3)
# c=map(lambda x:x**2,range(7))
# print(type(a))
# print(type(b))
#
# # print(type(a))
# d=1
# print(type(d))


# a=list(map(lambda x:float(x),['1','2']))
# print(a)



# class kobe:
#     a=1
# a=kobe()
# print(a.a)


#教育机构 ：马士兵教育
#讲    师：杨淑娟
# class Student:  #Student为类的名称（类名）由一个或多个单词组成，每个单词的首字母大写，其余小写
#    native_pace='吉林'  #直接写在类里的变量，称为类属性
#    def __init__(self,name,age):
#        self.name=name    #self.name 称为实体属性  ，进行了 一个赋值的操作，将局部变量的name的值赋给实体属性
#        self.age=age
#
#    #实例方法
#    def eat(self):
#        print('学生在吃饭...')
#        print(self.name)
#        return 1
#
#     #静态方法
#    @staticmethod
#    def method():
#        print('我使用了statticmethod进行修饰，所以我是静态方法')
#
#     #类方法
#    @classmethod
#    def cm(cls):
#        print('我是类方法，因为我使用了classmethod进行修饰')
# #在类之外定义的称为函数，在类之内定义的称为方法
# def drink():
#     print('喝水')

# a=Student(1,2)
# a.eat()

#
# class example:
#
#     def kobe(self,name,li):
#         print(name,li)
#         print('111')
#         return 1
#     @staticmethod
#     def bryant():
#         print('我是静态方法')
#
#     @classmethod
#     def cm(cls):
#         print('我是类方法~')
#
# a=example()
# c=a.kobe(1,2)
# example.bryant()
#
# example.cm()

# class test1:
#     # def __init__(self,name,age):
#     #     self.name=name
#     #     self.age=age
#     def info(self):
#         print('我是一个信息')
#
# class test2(test1):
#     def __init__(self,name,age):
#         super().__init__()
#         self.name=1
#         self.age=2
# a=test2(1,2)
# print(a.name)
# a.info()


# class example:
#
#     def __call__(self, *args, **kwargs):
#         print(args[0])
#         print(kwargs['kwargs'])
#
# a=example()
# a(1,kwargs=3)
#
# a('1',kwargs='kobe')
#
# class test1:
#
#     def test2(self,a,b):
#         print(a)
#         print(b)
# c=test1()
# c.test2(1,2)


# class a():
#     pass
#
# class c():
#     pass
# class d(a,c):
#     def __init__(self,name):
#         self.name=name
#         print('1111')
#
#
# e=d(1)
# print(e.__dict__)
#
# print(e.__class__)
#
# print(d.__bases__)
#
#
# print(d.__base__)
#
# print(d.__mro__)

# class a:
#     def __init__(self,number):
#         self.number=number
#
#     def __add__(self, other):
#         return self.number+other.number
#
#
# c=a(1)
# d=a(2)
# print(c+d)
# class test:
#
#
#     def test1(self):
#         print('111')
#
#
#
#
# a=test()
# a.test1()

# a=[{'k':i} for i in range(10) if i]
# print(a)
# b=test
#
# print(b)
#
#
# class test2():
#     c=1
# d=test2
# print(d.c)

# class kobe:
#     def __init__(self,data):
#         self.data=data
#     def test(self):
#         return self.data==0
#
# a=kobe(1)
# if a.test():
#     print('aaa')
# else:
#     print('1111')



# class test:
#
#     def test1(self):
#         a=2
#         while True:
#             if a==1:
#
#                 print('i')
#                 return
#             else:
#                 print('1111')
# a=test()
# a.test1()


# a=lambda x:x**2
#
#
# b=map(lambda x:x**2,[1,2,32,])
# print(list(b))

# class test:
#
#     def __init__(self,name):
#         self.name=name
#     def test1(self):
#         print(self.name)


# a='abcde'
#
# b=[1,232,34232,2212,2313]
# print(b.sort())
# print(b)
# # for i in a:
#     b.insert(0,i)


# b=''.join(b)
# print(type(b))
# print(type(''))

# a={i:j for i,j in zip([1,23,2],[2,1,3])}
# print(a)

import hashlib

class qukuai:
    def __init__(self):
        pass


