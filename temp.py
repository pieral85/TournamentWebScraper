# class A(object):
#     def __init__(self):
#         self.x = 0
#
#
# class B(object):
#     a = A()
#
#     @staticmethod
#     def start():
#         print('1: ' + str(B.a.x))
#         B.inc(B.a)
#         print('2: ' + str(B.a.x))
#
#     @staticmethod
#     def inc(obj):
#         print('3: ' + str(obj.x))
#         obj.x += 1
#         print('4: ' + str(obj.x))
#
# b = B()
# b.start()

# ====================================

import os

# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.getcwd())
print(os.path.join(os.getcwd(), "toto", "tutu"))
os.makedirs(os.path.join(os.getcwd(), "data", "tournament_123", 'toto.txt'), exist_ok=True)

