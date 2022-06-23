import numpy as np
import torch
import torch.nn as nn
from torch.nn import functional as F


def test_LogSoftmax():
    v = torch.tensor([[1, 2, 3],
                      [2, 3, 4]], dtype=torch.float64)
    log_softmax = nn.LogSoftmax(dim=1)
    p1 = log_softmax(v)

    # equal
    p = torch.exp(v)
    p_s = p.sum(dim=1, keepdim=True)
    p2 = (p / p_s).log()

    assert torch.equal(log_softmax(v), p)


def test_NLLLoss():
    pred = torch.tensor([[0.1, 0.2, 0.3],
                         [0.9, 0.3, 0.6],
                         [0.1, 0.3, 0.5]])
    target = torch.tensor([1, 2, 0])
    l = nn.NLLLoss(reduction='mean')
    # l = nn.NLLLoss(reduction='mean', ignore_index=2)

    # equal
    p = pred.gather(1, target.unsqueeze(-1))
    # res = -1 * p.sum()
    res = -1 * p.mean()
    print(l(pred, target))
    print(res)


def test_CrossEntropyLoss():
    pred = torch.tensor([[0.1, 0.2, 0.3],
                         [0.9, 0.3, 0.6],
                         [0.1, 0.3, 0.5]])
    target = torch.tensor([1, 2, 0])

    cross_entropy_loss = nn.CrossEntropyLoss(ignore_index=2)

    # equal
    log_softmax = nn.LogSoftmax(dim=1)
    nllloss = nn.NLLLoss(ignore_index=2)
    res = nllloss(log_softmax(pred), target)

    print(cross_entropy_loss(pred, target))
    print(res)


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


if __name__ == '__main__':
    # test_LogSoftmax()
    # test_NLLLoss()
    # test_CrossEntropyLoss()
    test_BCEWithLogits()
