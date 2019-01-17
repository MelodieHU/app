import numpy as np
import torch
import os
import cv2
from models.model import UNet
from models.set2feat import PointNetCls

global_data_root = '/media/dev/Space2/paint/dataset/data/'

epoch_num = 10

def myapp():
    data = np.zeros((2,3,224,224))
    data = torch.tensor(data).float().cuda()
    model = UNet(num_classes=1).cuda()
    output = model(data)
    print(output.shape)

    data = torch.rand(4,3,1024).float().cuda()
    model = PointNetCls(k=4).cuda()
    output,_ = model(data)
    print(output.shape)


def getdata():
    def csv2npy(file):
        npydata = []
        with open(file, 'r') as f:
            data = f.readlines()
            for line in data:
                line = line.strip().split(',')
                line = [float(x) for x in line]
                line = np.array(line)
                npydata.append(line)
        npydata = np.array(npydata)
        return npydata

    root0 = global_data_root
    before_path = os.path.join(root0,'patch_vangogh_before')
    # after_path = os.path.join(root0,'patch_vangogh_after')
    # stroke_path = os.path.join(root0,'patch_vangogh_stroke')

    before_data, after_data, stroke_data = [],[],[]
    for root,dir,files in os.walk(before_path):
        for i,file in enumerate(files):
            before = os.path.join(root,file)
            after = os.path.join(before.replace('before','after')).replace('.jpg','_.png')
            stroke = str(os.path.join(before.replace('before','stroke')).split('.')[0])
            before_data.append(cv2.imread(before))
            after_data.append(cv2.imread(after))
            stroke_data.append(csv2npy(stroke))

    before_data = np.array(before_data)
    after_data = np.array(after_data)
    stroke_data = np.array(stroke_data)
    np.save(os.path.join(root0,'before'),before_data)
    np.save(os.path.join(root0,'after'),after_data)
    np.save(os.path.join(root0,'stroke'),stroke_data)
