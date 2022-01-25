import time
import functools


# 1
def log(func):
    def wrap(*args, **kwargs):
        print(f'in wrap')
        return func()

    return wrap
@log
def now():
    print(f'now is: {time.time()}')


# 2
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper


# 3
# decorator with parameter
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


# 4
def method_decorator(method):
    def inner(city_instance):
        if city_instance.name == "SFO":
            print("Its a cool place to live in.")
        else:
            method(city_instance)
    return inner


class City(object):

    def __init__(self, name):
        self.name = name

    @method_decorator
    def print_test(self):
        print(self.name)

p1 = City("SFO")
p1.print_test()


# 5
class decoclass(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        # before f actions
        print('decorator initialised')
        self.f(*args, **kwargs)
        print('decorator terminated')
        # after f actions

@decoclass
def klass():
    print('class')

klass()


# 6
def makebold(f):
    return lambda: "<b>" + f() + "</b>"
def makeitalic(f):
    return lambda: "<i>" + f() + "</i>"

@makebold
@makeitalic
def say():
    return "Hello"

print(say())


# 7
class ClassDecorator(object):

    def __init__(self, arg1, arg2):
        print("Arguements passed to decorator %s and %s" % (arg1, arg2))
        self.arg1 = arg1
        self.arg2 = arg2

    def __call__(self, foo, *args, **kwargs):

        def inner_func(*args, **kwargs):
            print("Args passed inside decorated function .%s and %s" % (self.arg1, self.arg2))
            return foo(*args, **kwargs)
        return inner_func

@ClassDecorator("arg1", "arg2")
def print_args(*args):
    for arg in args:
        print(arg)

print_args(1, 2, 3)
