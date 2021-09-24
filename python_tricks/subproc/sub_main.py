import subprocess


def popen_process(command):
    p = subprocess.Popen(command, shell=True,
                        #  stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding='utf-8')

    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print('err')
        print(stderr)
    else:
        print('succ')
        # print(stdout)


if __name__ == '__main__':
    command = f'python main.py'

    popen_process(command)
