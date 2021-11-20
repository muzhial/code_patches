from parser import EasyDict


class TestDict(dict):

    def __init__(self, v):
        self.v = v

    def __setattr__(self, name, value):
        print(name, value)
        super().__setattr__(name, value)


def test():
    test1 = {
        'a': 1,
        'b': {
            'c': 2
        }
    }
    test1 = EasyDict(test1)
    # test1.__setattr__('d', 3)
    print(test1)


if __name__ == '__main__':
    test()
