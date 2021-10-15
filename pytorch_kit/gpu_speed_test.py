import time
import functools

import torch
from torch._C import device
import torch.nn as nn


def time_count(device):
    def decorator(fn):
        @functools.wraps(fn)
        def time_print(*args, **kwargs):
            if device == 'cpu':
                start_t = time.time()
                fn(*args, **kwargs)
                return time.time() - start_t  # s
            elif device == 'gpu':
                start = torch.cuda.Event(enable_timing=True)
                end = torch.cuda.Event(enable_timing=True)
                start.record()
                fn(*args, **kwargs)
                end.record()
                torch.cuda.synchronize()
                return start.elapsed_time(end) * 1e-3  # s
        return time_print
    return decorator

@time_count('gpu')
def copy_data(v):
    j = v.to('cuda:0')

@time_count('gpu')
def element_wise_multi(a, b):
    for _ in range(100):
        c = a * b

@time_count('gpu')
def tensor_slice_assignment(a, device):
    b = torch.randint(16, size=(1024, 2048))
    if device.startswith('cuda'):
        a = a.to(device)
        b = b.to(device)
    for _ in range(100):
        a[:, :, :, :] = b


if __name__ == '__main__':
    device = 'cuda:0'

    # a = torch.randn(3, 64, 1024, 1024)
    # b = torch.randn(64, 1024, 1024)
    # tm = copy_data(a)
    # print(f'copy: {tm}')

    # tm = element_wise_multi(a, b)
    # print(f'ele-wise multi@cpu: {tm}')

    # a = a.to(device)
    # b = b.to(device)
    # tm = element_wise_multi(a, b)
    # print(f'ele-wise multi@gpu: {tm}')

    m = torch.randn(3, 64, 1024, 2048)

    tm = tensor_slice_assignment(m, 'cpu')
    print(f'assignment: {tm}')
