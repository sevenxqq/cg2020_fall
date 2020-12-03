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
                for item_type, p_list, algorithm, color, res in item_dict.values():
                    for x,y in res:
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
                p_list = [[x0, y0], [x1, y1]]
                res = alg.draw_line(p_list, algorithm)
                item_dict[item_id] = ['line', p_list, algorithm, np.array(pen_color),res]
            elif line[0] == 'drawEllipse':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = 0
                p_list = [[x0, y0], [x1, y1]]
                res = alg.draw_ellipse(p_list)
                item_dict[item_id] = ['ellipse', p_list, algorithm, np.array(pen_color),res]
            elif line[0] == 'drawPolygon':
                item_id = line[1]
                length = len(line)
                pixlist = []
                i = 2
                while i < length-2:
                    pixlist.append((int(line[i]),int(line[i+1])))
                    i+=2
                algorithm = line[length-1]
                res = alg.draw_polygon(pixlist, algorithm)
                item_dict[item_id] = ['polygon', pixlist, algorithm, np.array(pen_color),res]
            elif line[0] == 'drawCurve':
                item_id = line[1]
                length = len(line)
                pixlist = []
                i = 2
                while i < length-2:
                    pixlist.append((int(line[i]),int(line[i+1])))
                    i+=2
                algorithm = line[length-1]
                res = alg.draw_curve(pixlist, algorithm)
                item_dict[item_id] = ['curve', pixlist, algorithm, np.array(pen_color),res]
            elif line[0] == 'translate':
                item_id = line[1]
                x = int(line[2])
                y = int(line[3])
                res = alg.translate(item_dict[item_id][4],x,y)
                item_dict[item_id][4] = res
            elif line[0] == 'rotate':
                item_id = line[1]
                if item_dict[item_id][0] !='ellipse':
                    x = int(line[2])
                    y = int(line[3])
                    r = int(line[4])
                    res = alg.rotate(item_dict[item_id][4],x,y,r)
                    item_dict[item_id][4] = res
            elif line[0] == 'scale':
                item_id = line[1]
                x = int(line[2])
                y = int(line[3])
                s = float(line[4])
                res = alg.scale(item_dict[item_id][4],x,y,s)
                item_dict[item_id][4] = res
            elif line[0] == 'clip':
                print("执行clip命令")
                item_id = line[1]
                a = int(line[2])
                b = int(line[3])
                c = int(line[4])
                d = int(line[5])
                algorithm = line[6]
                res = alg.clip(item_dict[item_id][1],a,b,c,d,algorithm)
                item_dict[item_id][4] = res
            ...

            line = fp.readline()

