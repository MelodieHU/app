#!/usr/bin/env python
import numpy
from time import time
import sys
import os
import gc
import csv
import pandas as pd

#os.chdir(os.path.dirname()) #sys.argv[0])
#sys.path.insert(0, '..')
sys.path.append('libs/mypaint')
from lib import mypaintlib, tiledsurface, brush, document, command, helpers

def brushPaint(filename):
    RADIUS_1 = 24
    RADIUS_2 = 12
    RADIUS_3 = 4

    s = tiledsurface.Surface()
    bi = brush.BrushInfo(open('brushes/watercolor_expressive.myb').read())
    b = brush.Brush(bi)
    Poids = 3
    #events = numpy.loadtxt('painting_test.dat')
    events = csv.reader(open(filename))
    t0 = time()
    t_old = 0.0
    t = 0.0
    i = 0
    pressure = 1.0
    for row in events:
        j = 0
        pos = []
        while j < len(row)-4:
            pos.append(int(row[j]))
            j += 1
        #x0, y0 = int(row[0]),int(row[1])
        #x1, y1 = int(row[2]),int(row[3])
        R,G,B = float(row[j]),float(row[j+1]),float(row[j+2])
        radius = int(row[j+3])
        if radius == RADIUS_1:
            pressure = 1.0
        elif radius == RADIUS_2:
            pressure = 0.9
        else:
            pressure = 0.8
        bi.set_color_rgb((R,G,B))
        dtime = 0.1
        k = 0
        while k < len(pos):
            s.begin_atomic()
            b.stroke_to(s.backend, pos[k]*Poids, pos[k+1]*Poids, pressure, 0.0, 0.0, dtime)
            dtime += 0.1
            s.end_atomic()
            k += 2
        b.reset()
        #print s.get_bbox(), b.get_total_stroke_painting_time()

        i += 1
        if i%100 == 0:
            print('row=',row)
            print s.get_bbox(), b.get_total_stroke_painting_time()
            img_name = 'test_brushPaint_'+str(i)+'.png'
            s.save_as_png(img_name)
    #s.save_as_png('test_brushPaint.png')

    print 'Brushpaint time:', time()-t0
    print s.get_bbox(), b.get_total_stroke_painting_time()  # FIXME: why is this time so different each run?

    s.save_as_png('test_brushPaint.png')


if __name__ == '__main__':
    brushPaint("62_0001")
    print 'Tests passed.'


