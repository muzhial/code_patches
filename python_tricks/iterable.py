import collections


a = range(11)
print(isinstance(a, collections.Iterable))  # True
print(isinstance(a, collections.Iterator))  # False

class IterableObj:
    def __iter__(self):
        return self

    
it = IterableObj()

print(isinstance(it, collections.Iterable))  # True
print(isinstance(it, collections.Iterator))  # False

