import torch


@torch.jit.script
def foo(len):
    # type: (int) -> torch.Tensor
    rv = torch.zeros(3, 4)
    for i in range(len):
        if i < 10:
            rv = rv - 1.0
        else:
            rv = rv + 1.0
    return rv
print('*' * 11)
print(foo.graph)


# torch.jit.frontend.NotSupportedError **kwargs
# @torch.jit.script
# def bar(len, **kwargs):
#     rv = torch.zeros(3, 4)
#     for i in range(len):
#         if i < 10:
#             rv = rv - 1.0
#         else:
#             rv = rv + 1.0
#     return rv


class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.x = 2

    def forward(self, a):
        print(self.config)
        return a

    @property
    def config(self):
        return {
            'key': 'value'
        }

print('*' * 11)
m = torch.jit.script(Model())
# print(m())
# m.save('./jit.pth')
# m = torch.jit.load('./jit.pth')
print(m(torch.tensor(0)))
m = torch.jit.trace(Model(), torch.tensor(0))
print(m(torch.tensor(3.3)))
