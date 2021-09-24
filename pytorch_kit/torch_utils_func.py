import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.utils.prune as prune


def test_op(net):
    for name, mod in net.named_modules():
        if isinstance(mod, nn.Conv2d):
            print(name)
            print(mod.weight.shape, mod.bias.shape)
            for b in mod.buffers():
                print(f'==> {b}')
        elif isinstance(mod, nn.ReLU):
            for b in mod.buffers():
                print(f'==> {b}')
        else:
            pass


def test_bn():
    bn = nn.BatchNorm2d(2)
    print(bn.weight)
    print(bn.bias)
    for n, b in bn.named_buffers():
        print(n, b.shape, b.requires_grad)


def test_prune():
    c1 = nn.Conv2d(1, 3, 3)
    print(c1.weight)
    print(c1.bias)

    prune.random_structured(c1, 'weight', 0.3)

    print(c1.weight)
    print(c1.bias)


def muzhi_0():
    v1 = torch.tensor([1.0, 3.0], requires_grad=True)
    v2 = v1 + 1
    loss = v2.mean()
    v2[0] = 5.0
    loss.backward()
    print(v1)
    print(v1.grad)


def func_tool():
    a = torch.rand(2, 3)
    print(a)
    sorted_a, sorted_idx = torch.sort(a, dim=0, descending=True)
    print(sorted_a)
    print(sorted_idx)
    print(a)
