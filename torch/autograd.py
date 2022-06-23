import torch
from torch.autograd.function import Function


class Exp(Function):

    @staticmethod
    def forward(ctx, i):
        result = i.exp()
        ctx.save_for_backward(result)
        return result

    @staticmethod
    def backward(ctx, grad_output):
        result, = ctx.saved_tensors
        return grad_output * result


x = torch.tensor([1.], requires_grad=True)
ret = Exp.apply(x)
print(ret)
ret.backward()
print(x.grad)
