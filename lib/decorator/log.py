# coding=utf-8
"""
调试用的日志装饰器

__author__ = 'zengyuetian'

"""


def log_func_args(function):
    """
    为调用的函数打印函数名，参数
    """
    def wrapper(*args, **kwargs):
        # Log Function name and Arguments
        print "[" + function.__name__ + "]", args, kwargs
        return function(*args, **kwargs)
    return wrapper


@log_func_args
def function_for_test(test1, test2):
    print "Function start"
    print "Function end"

if __name__ == "__main__":
    function_for_test(1, 2)