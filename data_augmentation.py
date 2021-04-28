import torch
import torchvision
from torchvision import transforms
from torchvision.utils import save_image
import os
import matplotlib.pyplot as plt



transform = transforms.Compose([
    transforms.Resize((32,32)),
    transforms.ColorJitter(),
    transforms.RandomGrayscale(),
    transforms.GaussianBlur((1,5)),
    transforms.ToTensor(),
])


train_path = './data'
classes = [class_dir for class_dir in os.listdir(train_path)]

trainset = torchvision.datasets.ImageFolder(train_path, transform=transform)

print(trainset.class_to_idx)
# for i in range(2):
for image, label in trainset:
    if classes[label] == 'Shade':
        print('fist !')
        to_pil = torchvision.transforms.ToPILImage()
        img = to_pil(image)
        plt.imshow(img)
        plt.show()
    # img_dir = os.path.join(train_path, classes[label], str(i)+'.png')
    # print(classes[label], img_dir)
    # save_image(image, img_dir)