'''
post_training_quantize

if using_bn:
    model = NetBN()
else:
    model = Net()

model.quantize(num_bits=num_bits)
model.eval()

for i, (data, target) in enumerate(train_loader, 1):
    output = model.quantize_forward(data)
    if i % 500 == 0:
        break
print('direct quantization finish')

model.freeze()

for i, (data, target) in enumerate(test_loader, 1):
    output = model.quantize_inference(data)
    pred = output.argmax(dim=1, keepdim=True)
    correct += pred.eq(target.view_as(pred)).sum().item()
'''