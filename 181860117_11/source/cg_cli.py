#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import cg_algorithms as alg
import numpy as np
from PIL import Image


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    item_dict = {}
    pen_color = np.zeros(3, np.uint8)
    width = 0
    height = 0

    with open(input_file, 'r') as fp:
        line = fp.readline()
        while line:
            line = line.strip().split(' ')
            if line[0] == 'resetCanvas':
                width = int(line[1])
                height = int(line[2])
                item_dict = {}
            elif line[0] == 'saveCanvas':
                save_name = line[1]
                canvas = np.zeros([height, width, 3], np.uint8)
                canvas.fill(255)
                for item_type, p_list, algorithm, color in item_dict.values():
                    if item_type == 'line':
                        pixels = alg.draw_line(p_list, algorithm)
                        for x, y in pixels:
                            canvas[y,x] = color 
                    elif item_type == 'polygon':
                        pixels = alg.draw_polygon(p_list, algorithm)
                        for x, y in pixels:
                            canvas[y,x] = color 
                    elif item_type == 'ellipse':
                        print("测试椭圆")
                        pixels = alg.draw_ellipse(p_list)
                        for x, y in pixels:
                            canvas[int(y),int(x)] = color 
                    elif item_type == 'curve':
                        pixels = alg.draw_curve(p_list, algorithm)
                        for x, y in pixels:
                            # print("当前打印",x,y,color)
                            canvas[int(y),int(x)] = color 
                Image.fromarray(canvas).save(os.path.join(output_dir, save_name + '.bmp'), 'bmp')
            elif line[0] == 'setColor':
                pen_color[0] = int(line[1])
                pen_color[1] = int(line[2])
                pen_color[2] = int(line[3])
            elif line[0] == 'drawLine':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = line[6]
                item_dict[item_id] = ['line', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
            elif line[0] == 'drawEllipse':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = 0
                item_dict[item_id] = ['ellipse', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
            elif line[0] == 'drawPolygon':
                item_id = line[1]
                length = len(line)
                pixlist = []
                i = 2
                while i < length-2:
                    pixlist.append((int(line[i]),int(line[i+1])))
                    i+=2
                algorithm = line[length-1]
                item_dict[item_id] = ['polygon', pixlist, algorithm, np.array(pen_color)]
            elif line[0] == 'drawCurve':
                item_id = line[1]
                length = len(line)
                pixlist = []
                i = 2
                while i < length-2:
                    pixlist.append((int(line[i]),int(line[i+1])))
                    i+=2
                algorithm = line[length-1]
                item_dict[item_id] = ['curve', pixlist, algorithm, np.array(pen_color)]
            ...

            line = fp.readline()

