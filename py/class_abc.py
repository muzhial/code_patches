class A:

    def fun1(self, op1, op2):
        print(f'from {self.__class__.__name__} -> fun1')
    
    def fun2(self, op1):
        print(f'from {self.__class__.__name__} -> fun2')

class B(A):

    def fun1(self):
        print(f'from {self.__class__.__name__} -> fun1')
    
    def fun3(self):
        print(f'from {self.__class__.__name__} -> fun3')


class BaseData:
    PALETTE = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    CLASSES = ['background', 'person']
    COLORS = None

    def __init__(self):
        self.CLASSES = ['mu', 'zhi']
        self.COLORS = ['blue']

class CData(BaseData):
    COLORS = ['brown']

    def __init__(self):
        super(CData, self).__init__()

class Fac:
    def __init__(self):
        print('Fac init')

class SubFac1(Fac):
    def __init__(self):
        # super(SubFac1, self).__init__()
        print('SubFac1 init')


if __name__ == '__main__':
    a = A()
    b = B()
    print(isinstance(b, A))  # True
    # a.fun1(1, 2)
    # b.fun1()
    # b.fun2(1)

    print('=' * 11)
    print(BaseData.PALETTE)
    print(BaseData.CLASSES)
    print(BaseData.COLORS)
    base = BaseData()
    print(base.CLASSES, BaseData.CLASSES)
    print(base.PALETTE)
    print(base.COLORS)
    base.COLORS = 'black'
    print(BaseData.COLORS)

    print('=' * 11)
    c = CData()
    print(c.COLORS, CData.COLORS)
