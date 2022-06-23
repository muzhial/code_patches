import torch.nn as nn
import torch


conv1 = nn.Conv2d(in_channels=3,
                  out_channels=32,
                  kernel_size=3,
                  stride=2,
                  padding=1,
                  bias=True)

print(conv1.weight.data.size())
print(conv1.bias.data.size())

# <class 'torch.nn.parameter.Parameter'> True
print(type(conv1.weight)
      ,conv1.weight.requires_grad)
# <class 'torch.Tensor'> False
print(type(conv1.weight.data)
      ,conv1.weight.data.requires_grad)


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
