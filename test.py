import torch
from torch.autograd import Variable
from tensorboardX import SummaryWriter
from models.model import UNet
from dataloader.loader import Mydata

global_data_root = './data/'
epoch_num = 10


def demo():
    Model = UNet(num_classes=3).cuda()
    DataLoader = Mydata.getLoader()
    Optimizer = torch.optim.Adam(Model.parameters())
    loss_fn = torch.nn.MSELoss()
    writer = SummaryWriter('./logs/test')
    for epoch in range(epoch_num):
        for (i,data) in enumerate(DataLoader):
            before = Variable(data[0]).cuda().float()
            after = Variable(data[1]).cuda().float()
            stroke = Variable(data[2]).cuda().float()

            before = before.permute(0,3,1,2)
            after = after.permute(0,3,1,2)
            stroke = stroke.permute(0,2,1)
            output = Model(before,stroke)

            loss = loss_fn(after,output)
            Optimizer.zero_grad()
            loss.backward()
            Optimizer.step()

            writer.add_scalar('loss',loss.item(),i)
            print(before.shape,output.shape,loss.item())


if __name__ == '__main__':
    demo()