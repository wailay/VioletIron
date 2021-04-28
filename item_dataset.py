from torch.utils.data import Dataset
from PIL import Image
import os

class ItemDataSet(Dataset):
    def __init__(self, data_dir, transform=None):
        self.img_labels = [label for label in os.listdir(data_dir)]
        self.label_to_idx = {label: i for i, label in enumerate(self.img_labels)}
        self.data_dir = data_dir
        self.transform = transform
        self.path_to_label = self.generate_dataset()

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path, label_name = self.path_to_label[idx]
        full_img_path = os.path.join(self.data_dir,label_name, img_path)
        
        img = None
        with open(full_img_path, 'rb') as f:
            img = Image.open(f)
            img = img.convert('RGB')
        
        if self.transform:
            img = self.transform(img)
        
        return img, self.label_to_idx[label_name]

        
    
    def generate_dataset(self):
        path_to_label = []
        for label_dir in os.listdir(self.data_dir):
            label_dir_path = os.path.join(self.data_dir, label_dir);
            for img_path in os.listdir(label_dir_path):
                path_to_label.append((img_path, label_dir))

        return path_to_label
        

if __name__ == '__main__':
    print('dataset test')
    
    

    