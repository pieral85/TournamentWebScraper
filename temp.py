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

def getRoundCoord(coord, offset, recursive=False):
    if offset > 0:
        return (coord[0] + 1, coord[1] // 2)
    else:
        if coord[0] <= 0:
            return None
        return[(coord[0] - 1, coord[1] * 2),
               (coord[0] - 1, coord[1] * 2 + 1)]

coord = (1, 3)
next_coord = (coord[0]+1, coord[1]//2)
if coord[0] > 0:
    prev_coord = [(coord[0]-1, coord[1]*2),
                  (coord[0]-1, coord[1]*2+1)]
else:
    prev_coord = None

print('=== ' + coord + ' ===',
      next_coord,
      prev_coord,
      sep='\n')
