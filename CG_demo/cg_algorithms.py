#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    if len(p_list) !=2:
        return []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    result = []
    """
        :处理特殊的直线
        :竖直线
        :水平线
        :对角线
    """
    if x0 == x1:
        if y0 > y1:
            y0, y1 = y1, y0
        for y in range(int(y0), int(y1 + 1)):
            result.append([x0, y])
        return result
    elif y0 == y1:
        if x0 > x1:
            x0, x1 = x1, x0
        for x in range(x0, x1 + 1):
            result.append([x, y0])
        return result
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    k = (y1 - y0) / (x1 - x0)
    if k == 1 and x0 == y0:
        for x in range(x0, x1 + 1):
            result.append([x, x])
        return result
    elif k == -1 and x0 == -y0:
        for x in range(x0, x1 + 1):
            result.append([x, -x])
        return result
    """
    :根据不同算法生成直线
    """
    if algorithm == 'Naive':
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        k = (y1 - y0) / (x1 - x0)
        for x in range(x0, x1 + 1):
            result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        """
        : 为了让点更密集，当k绝对值>1时将x y反转
        """
        if k > -1 and k < 1:
            for x in range(int(x0), int(x1 + 1)):
                y = k * (x - x0) + y0
                result.append([x, int(y)])
        else:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            t = (x1 - x0) / (y1 - y0)
            for y in range(y0, y1 + 1):
                result.append([int(x0 + t * (y - y0)), y])
    elif algorithm == 'Bresenham':
        if abs(k) < 1:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            dirtion = 1
            if k < 0:
                dirtion = -1
            dx = x1 - x0
            dy = y1 - y0
            dy2 = dy * 2
            dy2dx = dy2 - dx * 2 * dirtion
            pk = dy2 - dx * dirtion
            y = y0 - 1
            for x in range(int(x0), int(x1 + 1), dirtion):
                if pk >= 0:
                    y += 1
                    pk += dy2dx
                    result.append([int(x), int(y)])
                else:
                    pk += dy2
                    result.append([int(x), int(y)])
        else:
            dirtion = 1
            if k < 0:
                dirtion = -1
            dx = x1 - x0
            dy = y1 - y0
            dx2 = dx * 2
            dy2dx = dx2 - dy * 2 * dirtion
            pk = dx2 - dy * dirtion
            x = x0 - 1
            for y in range(int(y0), int(y1 + 1), dirtion):
                if pk < 0:
                    pk += dx2
                    result.append([int(x), int(y)])
                else:
                    x += 1
                    pk += dy2dx
                    result.append([int(x), int(y)])

    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标;
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    #计算椭圆中心和rx,ry
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    xc = (x0 + x1) / 2
    yc = (y0 + y1) / 2
    rx = abs(x1 - xc)
    ry = abs(y1 - yc)
    rx2 = pow(rx, 2)
    ry2 = pow(ry, 2)
    x = 0
    y = ry
    pk = ry2 - rx2 * ry + rx2 / 4
    #####区域1
    while ry2 * (x + 1) < rx2 * (y - 0.5):
        if pk < 0:
            pk += ry2 * (2 * x + 3)
            x += 1
            result.append([x, y])
        else:
            pk += ry2 * (2 * x + 3) + rx2 * (2 - 2 * y)
            x += 1
            y -= 1
            result.append([x, y])
    pk = ry * (x + 0.5) * 2 + rx * 2 * (y - 1) - rx * 2 * ry
    ###区域2
    while y > 0:
        if pk < 0:
            x += 1
            y -= 1
            pk += 2 * ry2 * x - 2 * rx2 * y + rx2
            result.append([x, y])
        else:
            y -= 1
            pk += rx2 - 2 * rx2 * y
            result.append([x, y])
    ###加入对称点
    length = len(result)
    for i in range(length):
        basex, basey = result[i]
        result.append([-basex + xc, basey + yc])
        result.append([-basex + xc, -basey + yc])
        result.append([basex + xc, -basey + yc])
        result[i] = [basex + xc, basey + yc]
    return result


####################----------------------############
#计算C(n,m)
def comb(n, m):
    return math.factorial(n) // (math.factorial(n - m) * math.factorial(m))


def bezier_alg(p_list, sz, step, startx):
    ans = []
    t = float(0)
    while (t < 1):
        x = float(0)
        y = float(0)
        for i in range(0, sz + 1, 1):
            x += comb(sz, i) * pow(t, i) * pow(1 - t, sz - i) * p_list[i][0]
            y += comb(sz, i) * pow(t, i) * pow(1 - t, sz - i) * p_list[i][1]
        ans.append([x, y])
        t += step
    return ans


#计算N(i,p)(u),para: ctrlnum,i,p,u,节点向量从 0->n+p,ui = i
def getcox(i, p, u):
    ans = float(0)
    if p == 0:
        if u >= i and u < i + 1:
            return 1
        return 0
    ans = ans + (u - i) / p * getcox(i, p - 1, u) + (i + p + 1 - u) / p * getcox(i + 1, p - 1, u)
    return ans


#para:ctrlpoint,n,p
def bspline_alg(p_list, n, p, step):
    res = []
    u = float(3)
    while (u < n):
        x = float(0)
        y = float(0)
        val = []
        for i in range(0, n, 1):
            temp = getcox(i, p, u)
            val.append(temp)
        for i in range(0, n, 1):
            x += p_list[i][0] * val[i]
            y += p_list[i][1] * val[i]
        res.append([x, y])
        u += step
    return res



def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    if algorithm == "Bezier" or algorithm == 'bezier':
        result = bezier_alg(p_list, len(p_list) - 1, 0.001, p_list[0][0])
        return result
    elif algorithm == "B-spline" or algorithm == 'b-spline':
        result = bspline_alg(p_list, len(p_list), 3, 0.001)
        return result
    pass


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元点集
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    res = []
    for i in range(len(p_list)):
        res.append([p_list[i][0] + dx, p_list[i][1] + dy])
    return res


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    radr = float(r)
    radr = radr * math.pi / 180
    res = []
    for oldx,oldy in p_list:
        x1 = float((oldx - x) * math.cos(radr)) - float((oldy - y) * math.sin(radr)) + float(x)
        y1 = float((oldx - x) * math.sin(radr)) + float((oldy - y) * math.cos(radr)) + float(y)
        res.append([x1,y1])
    return res


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元点集
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for i in range(len(p_list)):
        p_list[i][0] = p_list[i][0] - x
        p_list[i][1] = p_list[i][1] - y
    for i in range(len(p_list)):
        p_list[i][0] = p_list[i][0] * s
        p_list[i][1] = p_list[i][1] * s
    for i in range(len(p_list)):
        p_list[i][0] = p_list[i][0] + x
        p_list[i][1] = p_list[i][1] + y
    return p_list

#function for clip
def getCsCode(x, y, x_min, y_min, x_max, y_max):
    res = 0
    if x < x_min:
        res += 1
    if x > x_max:
        res += 2
    if y < y_min:
        res += 4
    if y > y_max:
        res += 8
    return res


def getval(x0, y0, x1, y1, x_min, y_min, x_max, y_max):
    detax = x1 - x0
    detay = y1 - y0
    p1 = -detax
    q1 = x0 - x_min
    p2 = detax
    q2 = x_max - x0
    p3 = -detay
    q3 = y0 - y_min
    p4 = detay
    q4 = y_max - y0
    p = []
    p.extend([0, p1, p2, p3, p4])
    q = []
    q.extend([0, q1, q2, q3, q4])
    return detax, detay, p, q


def calu(u1, u2, p, q):
    for i in range(1, 5, 1):
        if p[i] < 0:
            u1 = max(u1, float(q[i] / p[i]))
        elif p[i] > 0:
            u2 = min(u2, float(q[i] / p[i]))
    return u1, u2


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = [[0,0],[0,0]]
    if algorithm == "Cohen-Sutherland":
        q_list = [[x0,y0],[x1,y1]]
        code1 = getCsCode(x0, y0, x_min, y_min, x_max, y_max)
        code2 = getCsCode(x1, y1, x_min, y_min, x_max, y_max)
        while (True):
            x0, y0, x1, y1 = q_list[0][0], q_list[0][1], q_list[1][0], q_list[1][1]
            if (code1 | code2) == 0:
                return q_list
            elif (code1 & code2) != 0:
                return result
            else:
                if x0 == x1:
                    if x0<x_min or x0 > x_max:
                        return result
                    if y0 > y1:
                        y0,y1 = y1,y0
                    if y0 > y_max or y1 < y_min:
                        return result
                    y0 = max(y0,y_min)
                    y1 = min(y1,y_max)
                    q_list = [[x0,y0],x1,y1]
                    return q_list
                elif y0 == y1:
                    if y0<y_min or y0 > y_max:
                        return result
                    if x0 > x1:
                        x0,x1 = x1,x0
                    if x0 > x_max or x1 < x_min:
                        return result
                    x0 = max(x0,x_min)
                    x1 = min(x1,x_max)
                    q_list = [[x0,y0],x1,y1]
                    return q_list
                k = (y1 - y0) / (x1 - x0)
                code = code1
                if code1 == 0:  # 选可见的点
                    code = code2
                if (code & 0x01) != 0:  # 线段与窗口的左边有交
                    print("left")
                    x = x_min
                    y = y0 + int((x - x0) * k)
                elif (code & 0x02) != 0:  # 线段与窗口的右边有交
                    print("right")
                    x = x_max
                    y = y0 + int((x - x0) * k)
                elif (code & 0x04) != 0:  # 线段与窗口的下边有交
                    print("down")
                    y = y_min
                    x = x0 + int((y - y0) / k)
                elif (code & 0x08) != 0:  # 线段与窗口的上边有交
                    print("up")
                    y = y_max
                    x = x0 + int((y - y0) / k)
                if code == code1:  #更新新端点值
                    code1 = getCsCode(x, y, x_min, y_min, x_max, y_max)
                    q_list[0] = [x, y]
                else:
                    code2 = getCsCode(x, y, x_min, y_min, x_max, y_max)
                    q_list[1] = [x, y]
        return result
    elif algorithm == "Liang-Barsky":
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        detax, detay, p, q = getval(x0, y0, x1, y1, x_min, y_min, x_max, y_max)
        umax = float(0)
        umin = float(1)
        if detax == 0 and (q[1] < 0 or q[2] < 0):
            return result
        elif detay == 0 and (q[3] < 0 or q[4] < 0):
            return result
        else:
            umax, umin = calu(umax, umin, p, q)
            if umax > umin:
                return result
            else:
                x3 = int(x0 + umax * detax)
                y3 = int(y0 + umax * detay)
                x4 = int(x0 + umin * detax)
                y4 = int(y0 + umin * detay)
                q_list = []
                q_list.extend([[x3, y3], [x4, y4]])
                return q_list
    pass
