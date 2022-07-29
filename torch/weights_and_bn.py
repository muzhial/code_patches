import torch.nn as nn
import torch


def test_conv_weights():
    conv1 = nn.Conv2d(in_channels=3,
                      out_channels=32,
                      kernel_size=3,
                      stride=2,
                      padding=1,
                      bias=True)

    print(conv1.weight.data.size())
    print(conv1.bias.data.size())

    # <class 'torch.nn.parameter.Parameter'> True
    print(type(conv1.weight), conv1.weight.requires_grad)
      # <class 'torch.Tensor'> False
    print(type(conv1.weight.data) ,conv1.weight.data.requires_grad)


def test_bn_forward():
    x = torch.tensor([[[[1., 2., 3.],
                      [1., 2., 3.],
                      [1., 2., 3.]],

                      [[2., 2., 2.],
                      [3., 1., 1.],
                      [5., 4., 3.]],

                      [[1., 1., 1.],
                      [5., 6., 8.],
                      [9., 0., 1.]]]])
    mean_c = x.mean(dim=(0, 2, 3), keepdim=True)
    # std_c = x.std(dim=(0, 2, 3), keepdim=True)
    std_c = x.var(dim=(0, 2, 3), unbiased=False, keepdim=True)
    print("x:")
    print(x)
    print("x channel mean:")
    print(mean_c)
    print("x channel std:")
    print(std_c)
    print((x - mean_c) / torch.sqrt(std_c + 1e-5))


    v = nn.BatchNorm2d(3, affine=False)
    # # for p in v.named_parameters():
    # #     print(p)
    # # for b in v.named_buffers():
    # #     print(b)
    y = v(x)
    print("batch norm forward:")
    print(y)


def test_bn():
    torch.manual_seed(42)
    x = torch.randn(7, 3, 20, 20)
    bn = nn.BatchNorm2d(num_features=3)
    # 关闭 track_running_stats 后，即使在 eval 模式下，
    # 也会去计算输入的 mean 和 var。
    bn1 = nn.BatchNorm2d(num_features=3, track_running_stats=False)
    bn1.eval()
    print(bn.track_running_stats, bn.affine)
    print(bn.running_mean, bn.running_var)
    y = bn(x)
    print(bn.running_mean, bn.running_var)
    print('=' * 5)
    print(bn1.track_running_stats, bn1.affine)
    print(bn1.running_mean, bn1.running_var)
    y1 = bn1(x)
    print(bn1.running_mean, bn1.running_var)
    print(torch.allclose(y, y1))


class A:

    def __init__(self):
        self.w = torch.tensor([1], dtype=torch.float32, requires_grad=True)

    def forward(self, x):
        o = self.w * self.w * x
        o = 2 * o
        return o

def test_forward():
    a = A()
    for _ in range(3):
        x = torch.tensor([2])
        y = a.forward(x)
        # y.backward()
        print(a.w.grad)
        print(y)


if __name__ == '__main__':
    # test_bn()
    test_forward()
