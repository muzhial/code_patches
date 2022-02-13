import torch
import torch.nn as nn


# stack
def stack():
    y, x = torch.meshgrid([torch.arange(3), torch.arange(2)])
    print(y)
    print(x)
    z = torch.stack((x, y), dim=2)
    print(z)


def dim_op():
    a = torch.randn(3, 2)
    print(a[:, None].size())


if __name__ == '__main__':
    dim_op()
