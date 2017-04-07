from sqlalchemy.orm.collections import collection


class SetLike(object):
    __emulates__ = list # set

    def __init__(self):
        self.data = set()

    @collection.appender
    def append(self, item):
        self.data.add(item)

    @collection.remover
    def remove(self, item):
        self.data.remove(item)

    @collection.iterator
    def __iter__(self):
        return iter(self.data)
