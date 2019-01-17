import os
import numpy as np
import torch.utils.data as Data
from options.train_option import opt


class Mydata(Data.Dataset):
    def __init__(self):
        self.root = opt.data_root
        self.before_data = np.load(os.path.join(self.root,'before.npy'))
        self.after_data = np.load(os.path.join(self.root,'after.npy'))
        self.stroke_data = np.load(os.path.join(self.root,'stroke.npy'))

    def __getitem__(self, item):
        return self.before_data[item],self.after_data[item],self.stroke_data[item][:256][:,:3]

    def __len__(self):
        return len(self.before_data)

    @classmethod
    def getLoader(cls):
        dataset = cls()
        return Data.DataLoader(
            dataset = dataset,
            batch_size=8,
            shuffle=True,
            num_workers=4,
        )
