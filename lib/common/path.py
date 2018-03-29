# coding=utf-8
# __author__ = 'zengyuetian'

import inspect
import os
import sys


def get_root_path():
    """
    get the root path of auto test framework
    :return:
    """
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    lib_path = os.path.dirname(parent_path)
    root_path = os.path.dirname(lib_path)
    return root_path


def get_root_parent_path():
    """
    get the parent path of root auto test framework
    :return:
    """
    root_parent_path = os.path.dirname(get_root_path())
    return root_parent_path


def get_root_dir_name():
    """
    short name of root path
    :return:
    """
    return os.path.basename(get_root_path())

# root path
ROOT_PATH = get_root_path()

# result dir
RESULT_PATH = get_root_path() + "/result"

# misc dir
MISC_PATH = get_root_path() + "/misc"


###############################
# for debugging
###############################
if __name__ == "__main__":
    print get_root_path()
    print get_root_dir_name()



