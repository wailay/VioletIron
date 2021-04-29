import torch
import torchvision
from torchvision import transforms
import os
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from item_dataset import ItemDataSet




class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 13 * 13, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 59)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 13 * 13)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


if __name__ == '__main__':
    
    tensor = torch.rand(3, 2, 3,4)


    transform = transforms.Compose([
        transforms.ColorJitter(),
        transforms.Resize((64,64)),
        transforms.ToTensor()])

    train_path = './data'


    trainset = ItemDataSet(train_path, transform)
    
    batch_size = 4
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)


    classes = [class_dir for class_dir in os.listdir(train_path)]
    print(len(classes))


    net = Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(10):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 200 == 199:    # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                    (epoch + 1, i + 1, running_loss / 200))
                running_loss = 0.0

    print('Finished Training')


    PATH = './isaac_net.pth'
    torch.save(net.state_dict(), PATH)