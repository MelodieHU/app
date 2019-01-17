import torch
from torch.autograd import Variable
from tensorboardX import SummaryWriter

from models.model import UNet
from dataloader.loader import Mydata
from options.train_option import opt

def demo():
    Model = UNet(num_classes=3).cuda()
    DataLoader = Mydata.getLoader()
    Optimizer = torch.optim.Adam(Model.parameters())
    loss_fn = torch.nn.MSELoss()
    writer = SummaryWriter(opt.log_dir)
    for epoch in range(opt.epoch_num):
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