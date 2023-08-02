#codeing:utf-8
from comment.models import db
from sqlalchemy.util._collections import AbstractKeyedTuple
import datetime
import decimal

# 数据库返回数据list 转 dict

def datalist2dict(res_obj):
    if not res_obj:
        return None
    if isinstance(res_obj, list):  # 列表解析
        if len(res_obj) == 0:
            return None
        if isinstance(res_obj[0], AbstractKeyedTuple):  #
            dic_list = datalist_format([dict(zip(result.keys(), result)) for result in res_obj])
            return dic_list
        elif isinstance(res_obj[0], db.Model):
            [item.__dict__.pop("_sa_instance_state") for item in res_obj]
            return datalist_format([item.__dict__ for item in res_obj])
        elif isinstance(res_obj[0], dict):  #在db中存在json字段时返回的是dict
            return datalist_format(res_obj)
        else:
            return None
    else:
        return data2dict(res_obj)


# 数据库返回单个数据 转 dict

def data2dict(res_obj):
    if not res_obj:
        return None
    if isinstance(res_obj, dict):
        return res_obj
    elif isinstance(res_obj, AbstractKeyedTuple):
        dict_obj = data_format(dict(zip(res_obj.keys(), res_obj)))
        return dict_obj
    elif isinstance(res_obj, db.Model):
        res_obj.__dict__.pop("_sa_instance_state")
        return data_format(res_obj.__dict__)
    else:
        return None

"""
    列表 时间转字符串  Decimal转浮点型
    :param res: 列表
    :return:列表
"""
def datalist_format(reslist):
    if not reslist or not isinstance(reslist, list):
        return reslist
    for item in reslist:
        for key in item.keys():
            if isinstance(item[key], datetime.datetime) or isinstance(item[key], datetime.date):
                item[key] = str(item[key])
            if isinstance(item[key], decimal.Decimal):
                item[key] = float(item[key])
    return reslist

"""
    对象 中 时间转字符串 Decimal转浮点型
    :param bean: 传入dict
    :return:dict
"""
def data_format(bean):
    if not bean or not isinstance(bean, dict):
        return bean
    for key in bean.keys():
        if isinstance(bean[key], datetime.datetime) or isinstance(bean[key], datetime.date):
            bean[key] = str(bean[key])
        if isinstance(bean[key], decimal.Decimal):
            bean[key] = float(bean[key])
    return bean


class BasePaginateSerializer(object):
    """分页数据序列化基类"""

    def __init__(self, paginate):
        self.pg = paginate
        if not self.pg:
            return paginate
        self.has_next = self.pg.has_next  # 是否还有下一页
        self.has_prev = self.pg.has_prev  # 是否还有下一页
        self.next_num = self.pg.next_num  # 下一页的页码
        self.page = self.pg.page  # 当前页的页码
        self.pages = self.pg.pages  # 匹配的元素在当前配置一共有多少页
        self.total = self.pg.total  # 匹配的元素总数

    def get_object(self, obj):
        """对象的内容,系列化的个性操作,子类重写"""
        return {}

    #
    def paginateInfo(self):
        """分页信息，是否有上下页，页数，总页数等"""
        return {
            'has_next': self.has_next,
            'has_prev': self.has_prev,
            'next_num': self.next_num,
            'page': self.page,
            'pages': self.pages,
            'total': self.total
        }

    def to_dict(self):
        """序列化分页数据"""
        pg_info = self.paginateInfo()
        paginate_data = []
        for obj in self.pg.items:
            paginate_data.append(self.get_object(obj))
        return {
            'paginateInfo': pg_info,
            'totalElements': pg_info['total'],
            'content': paginate_data
        }


class BaseSerializer(object):
    """对象序列化基类"""
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        """个性化的系列化,子类重写 """
        return {}


class BaseListSerializer(object):
    """对象组序列化基类"""
    def __init__(self, data):
        self.data_list = data
        self.select_type_serializer()

    def select_type_serializer(self):
        if not self.data_list:
            return None
        if isinstance(self.data_list, list):  # 列表解析
            if len(self.data_list) == 0:
                return None
            if isinstance(self.data_list[0], AbstractKeyedTuple):  #
                self.data_list = [dict(zip(result.keys(), result)) for result in self.data_list]


    def to_dict(self):
        """个性化的系列化,子类重写 """
        return {}
