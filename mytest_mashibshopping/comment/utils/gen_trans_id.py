import random
import time
import datetime


def gen_trans_id(date=None):
    """ 生成交易流水号 """
    if date is None:

        date = datetime.datetime.now()
    str_date = date.strftime('%Y%m%d%H%M%S%f')
    a = str_date
    print(a)
    str_random = random.randint(1000, 9999)
    return '{}{}'.format(str_date, str_random)