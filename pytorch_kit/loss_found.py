import numpy as np
import torch
import torch.nn as nn


def test_BCEWithLogits():
    loss = nn.BCEWithLogitsLoss()
    i = torch.randn(5)
    t = torch.empty(5).random_(2)  # torch.float32
    o = loss(i, t)
    print(o)

    # equal
    si = -1 * t * i.sigmoid().log() - (1 - t) * (1 - i.sigmoid()).log()
    si = si.mean()
    print(si)

def test_():
    v = torch.tensor([[1, 2, 3],
                      [2, 3, 4]], dtype=torch.float64)
    v1 = nn.LogSoftmax(dim=1)
    print(v1(v))

    p = torch.exp(v)
    p_s = p.sum(dim=1, keepdim=True)
    p = (p / p_s).log()
    print(p)

    v = torch.tensor([[0.1, 0.2, 0.3],
                      [0.9, 0.3, 0.6],
                      [0.1, 0.3, 0.5]])
    v_t = torch.tensor([1, 2, 0])

    # l = nn.NLLLoss(reduction='sum')
    # l = nn.NLLLoss(reduction='mean', ignore_index=2)
    l = nn.NLLLoss(reduction='mean')
    res = l(v, v_t)
    print(res)

    p = v.gather(1, v_t.unsqueeze(-1))
    # res = -1 * p.sum()
    res = -1 * p.mean()
    print(res)

    l = nn.CrossEntropyLoss(ignore_index=2)
    res = l(v, v_t)
    print(res)

    l1 = nn.LogSoftmax()
    l2 = nn.NLLLoss(ignore_index=2)
    res = l1(v)
    res = l2(res, v_t)
    print(res)

    l = nn.NLLLoss(reduction='none')
    v1 = torch.rand(2, 3, 5, 5)
    print(v1)
    v2 = torch.zeros(2, 5, 5).random_(3).long()
    print(v2)
    print(l(v1, v2))

if __name__ == '__main__':
    test_BCEWithLogits()
