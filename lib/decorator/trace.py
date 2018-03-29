# coding=utf-8
"""
打印debug时出错信息的装饰器

__author__ = 'zengyuetian'

将其放在报错的函数上面
"""

import traceback

def print_trace(function):
    def wrapper(*args, **kw):
        try:
            return function(*args, **kw)
        except Exception, e:
            traceback.print_exc()
            print e.message
            raise e
    return wrapper



################################
# for unit testing
################################
@print_trace
def div_num(num1, num2):

    return num1/num2

if __name__ == "__main__":
    result = div_num(3, 2)
    print result
    result = div_num(2, 0)
    print result