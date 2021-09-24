import time


def log(func):
    def wrap(*args, **kwargs):
        print(f'in wrap')
        return func()

    return wrap

@log
def now():
    print(f'now is: {time.time()}')


if __name__ == '__main__':
    now()