# coding:utf-8
import os
import random
import cairo
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
import csv
import codecs

class Painter:
    def paint(self, src_name):
        # <PIL.Image.Image image mode=RGB size=1925x1280 at 0x10E92F278>
        src_file = "1_0001.jpg"
        src_img = Image.open(src_file).convert('RGB')
        

        self.canvas = cairo.ImageSurface(cairo.FORMAT_RGB24, src_img.width, src_img.height)
        self.context = cairo.Context(self.canvas)
        self.context.scale(src_img.width, src_img.height)
        self.context.set_line_cap(cairo.LINE_CAP_ROUND)

        filename = "62_0001"
        self.paintLayer(filename)
        
        self.canvas.write_to_png('./%s.png' % (src_name))
        return self.canvas

    def paintLayer(self, filename):
        events = csv.reader(open(filename))
        for row in events:
            j = 0
            S = []
            while j < len(row)-4:
                pair = []
                pair.append(int(row[j]))
                pair.append(int(row[j+1]))
                S.append(pair)
                j += 2

            R,G,B = float(row[j]),float(row[j+1]),float(row[j+2])
            radius = int(row[j+3])
            print(S)
            #for s in S:
            print(S)
            self.context.set_line_width(max(self.context.device_to_user_distance(2 * radius, 2 * radius)))
            #stroke_color = self.ref_nparray[s[0]]/255
            self.context.set_source_rgb(R, G, B)

            self.context.move_to(S[0][0] / self.canvas.get_width(), S[0][1] / self.canvas.get_height())
            for i in range(1, len(S)):
                self.context.line_to(S[i][0] / self.canvas.get_width(), S[i][1] / self.canvas.get_height())
                self.context.move_to(S[i][0] / self.canvas.get_width(), S[i][1] / self.canvas.get_height())

            self.context.close_path()
            self.context.stroke()


if __name__ == '__main__':
    painter = Painter()
    res = painter.paint('62_0001')
