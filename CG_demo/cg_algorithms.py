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
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
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
        for y in range(y0, y1 + 1):
            result.append((x0, y))
        return result
    elif y0 == y1:
        if x0 > x1:
            x0, x1 = x1, x0
        for x in range(x0, x1 + 1):
            result.append(x, y0)
        return result
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    k = (y1 - y0) / (x1 - x0)
    if k == 1 and x0==y0:
        for x in range(x0, x1 + 1):
            result.append((x, x))
        return result
    elif k == -1 and x0==-y0:
        for x in range(x0, x1 + 1):
            result.append((x, -x))
        return result
    """
    :根据不同算法生成直线
    """
    print("当前直线斜率为：", k)
    if algorithm == 'Naive':
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        k = (y1 - y0) / (x1 - x0)
        for x in range(x0, x1 + 1):
            result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        print("使用DDA算法")
        """
        : 为了让点更密集，当k绝对值>1时将x y反转
        """
        if k > -1 and k < 1:
            for x in range(x0, x1 + 1):
                y = k * (x - x0) + y0
                print("点对为",x,y)
                result.append((x, int(y)))
        else:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            t = (x1 - x0) / (y1 - y0)
            for y in range(y0, y1 + 1):
                result.append((int(x0 + t * (y - y0)), y))
    elif algorithm == 'Bresenham':
        """

        """
        print("使用Bresenham算法")
        if abs(k) < 1:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            dx = x1 - x0
            dy = y1 - y0
            detax = dx << 1
            detay = dy << 1
            pk = -dx
            y = y0
            dirtion = 1
            if k < 0:
                dirtion = -1
            for x in range(x0, x1 + 1, dirtion):
                pk += detay
                if pk > 0:
                    y += 1
                    pk -= detax
                result.append((x, y))
        else:
            dx = x1 - x0
            dy = y1 - y0
            detax = dx << 1
            detay = dy << 1
            pk = -dy
            x = x0
            dirtion = 1
            if k < 0:
                dirtion = -1
            for y in range(y0, y1 + 1, dirtion):
                pk += detax
                if pk > 0:
                    x += 1
                    pk -= detay
                result.append((x, y))
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
    pass


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    pass


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


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
    pass
