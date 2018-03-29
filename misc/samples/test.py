# coding=utf-8
# author: zengyuetian

from lib.control.const import *

l = [1, 2, 3, 4]
for i, j in enumerate(l):
    print i, j

my_dict = {
    "1": 10,
    "2": 20
}

for k in my_dict:
    print k

ret = False

my_list = [(1, 2), (3, 4)]
for i, j in my_list:
    print i, j

print("hello".upper())

# # check if all version exist
# version_set = set(PEER_VERSIONS)
# version_set.add(LF_VERSION)
# for v in version_set:
#     version_sdk = "{0}/sdk/{1}/{2}".format(MISC_PATH, v, SDK_FILE)
#     if not os.path.exists(version_sdk):
#         print ret
