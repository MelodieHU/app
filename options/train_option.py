import os
import argparse

class BaseOptions():
    def __init__(self):
        self.initialized = False
        self.log_dir = './logs/test{}'.format(len(os.listdir('./logs'))+1)
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)

    def initialize(self,parser):
        parser.add_argument('--data_root',type=str,default='./data')
        parser.add_argument('--batch_size',type=int,default=8)
        parser.add_argument('--epoch_num',type=int,default=24)
        parser.add_argument('--learning_rate',type=float,default=1e-3)
        parser.add_argument('--log_dir',type=str,default=self.log_dir)
        self.initialized = True
        return parser

    def print_options(self,opt):
        message = ''
        message += '---------------------Options------------------\n'
        for k,v in sorted(vars(opt).items()):
            comment = ''
            default = self.parser.get_default(k)
            if v != default:
                comment = '\t[default: %s]' % str(default)
            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v),comment)
        message += '----------------------End---------------------\n'
        print(message)

        opt_file = os.path.join(self.log_dir,'opt.txt')
        with open(opt_file,'w') as opt_file:
            opt_file.write(message)
            opt_file.write('\n')

    def parser(self):
        if not self.initialized:
            parser = argparse.ArgumentParser()
            parser = self.initialize(parser)
        opt,_ = parser.parse_known_args()
        self.parser = parser
        self.opt = opt
        self.print_options(self.opt)
        return self.opt

opt = BaseOptions().parser()


