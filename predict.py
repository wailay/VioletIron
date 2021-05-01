import torch
from torch.autograd import Variable
from cnn import Net
import torchvision
from torchvision import transforms
from PIL import Image
import os

NETPATH = './isaac_net.pth'
train_path = './data'
classes = [class_dir for class_dir in os.listdir(train_path)]

net = Net(len(classes))
net.load_state_dict(torch.load(NETPATH))

transform = transforms.Compose([
transforms.Resize((32,32)),
transforms.ToTensor()])


for img_path in os.listdir('./test'):
    img = Image.open(os.path.join('./test', img_path)).convert('RGB')
    img_tensor = transform(img).float()

    img_tensor = img_tensor.unsqueeze_(0)

    input=Variable(img_tensor)

    output = net(input)


    idx = output.data.numpy().argmax()


    print(img_path, classes[idx])
