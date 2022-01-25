import time
import functools

import torch
from torch._C import device
import torch.nn as nn


def tensor_slice_assignment(a, device):
    b = torch.randint(16, size=(1024, 2048))
    if device.startswith('cuda'):
        a = a.to(device)
        b = b.to(device)
    print("GPU occupied now ...")
    while True:
        # a[:, :, :, :] = b
        time.sleep(0.05)
        a = a * b


if __name__ == '__main__':
    device = 'cuda:0'

    m = torch.randn(3, 64, 1024, 2048)

    tm = tensor_slice_assignment(m, 'cuda:0')

