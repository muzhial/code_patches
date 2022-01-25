import time
import sys

def main():
    raise ValueError('test err')
    sys.stdout.write('sleep 3s start\n')
    time.sleep(3)
    sys.stdout.write('sleep 3s end\n')
    # sys.stdout.flush()
    


if __name__ == '__main__':
    main()
