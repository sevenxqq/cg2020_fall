#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
   
    QFileDialog,
    QColorDialog,
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPixmap
from PyQt5.QtCore import QRectF
import math

class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        #----------
        self.start_pos = None
        self.angel = None
        self.plist=None
        self.temp_col = QColor(0,0,255)

    def update_corlor(self,col):
        if self.status == 'polygon' or self.status == 'curve': #没画完就选择了变颜色
            self.finish_draw() 
        self.temp_col = col
    def reset_canvas(self):
        if self.status == 'polygon' or self.status == 'curve': #没画完就点击了重置
            self.finish_draw()
        for figure_item in self.item_dict:
            self.item_dict[figure_item].p_list = None
            self.updateScene([self.sceneRect()])
        self.item_dict = {}
        self.list_widget.clear()
    def save_canvas(self,filename,w,h):
        if self.status == 'polygon' or self.status == 'curve': #没画完就点击了保存
            self.finish_draw()
        painter = QPainter()
        pix = QPixmap(w, h)
        pix.fill(QColor(255,255,255))
        painter.begin(pix)
        for item in self.item_dict:
            self.item_dict[item].paint(painter,QStyleOptionGraphicsItem)
        painter.end()
        pix.save(filename)

    #设置item的各项参数
    def start_draw_figure(self, algorithm, item_id,figtype):
        if self.status == 'polygon' or self.status == 'curve': #没画完就点击画了别的图元
            self.finish_draw() #注意这里item_cnt会+1，而传入的temp_id是+1前的
            item_id+=1
        self.status = figtype
        self.temp_algorithm = algorithm
        self.temp_id = item_id


    def start_translate(self):
        if self.status == 'polygon' or self.status == 'curve': #没画完就选择了变换
            self.finish_draw() 
        if self.selected_id=='':
            self.status = ''
            return
        self.status = 'translate'
        self.temp_item=self.item_dict[self.selected_id]
        self.plist=self.temp_item.p_list

    def start_rotate(self):
        if self.status == 'polygon' or self.status == 'curve': #没画完就选择了变换
            self.finish_draw() 
        if self.selected_id=='':
            self.status = ''
            return
        if self.item_dict[self.selected_id].item_type == 'ellipse':
            self.status=''
            return
        self.status = 'rotate'
        self.temp_item=self.item_dict[self.selected_id]
        self.plist=self.temp_item.p_list
        self.angel=0

    def start_scale(self,scaletype):
        if self.status == 'polygon' or self.status == 'curve': #没画完就选择了变换
            self.finish_draw() 
        if self.selected_id=='':
            self.status = ''
            return
        self.status = scaletype
        self.temp_item=self.item_dict[self.selected_id]
        self.plist=self.temp_item.p_list

    def start_clip(self, algorithm):
        if self.status == 'polygon' or self.status == 'curve': #没画完就选择了变换
            self.finish_draw() 
        if self.selected_id=='':
            self.status = ''
            return
        if self.item_dict[self.selected_id].item_type != 'line':
            self.status=''
            return
        self.status = 'clip'
        self.temp_item=self.item_dict[self.selected_id]
        self.plist=self.temp_item.p_list
        self.temp_algorithm = algorithm




    #每一次inc_id所有的id编号就会自增一次
    def finish_draw(self):
        if self.temp_item != None and self.status!=None: 
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(str(self.temp_id))
            self.main_window.inc_id()
            self.temp_item = None
            self.status =None
    def finish_fluctuate(self):
        if self.temp_item != None and self.status!=None: 
            self.item_dict[self.selected_id] = self.temp_item
            self.temp_item = None
            self.status =None
            self.plist = None
            

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        if self.status == 'polygon' or self.status == 'curve': #没画完就选择了列表
            self.finish_draw() 
        selected = selected.text()
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        if selected == '':
            return
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.temp_item.setcor(self.temp_col)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon' or self.status == 'curve':
            if self.temp_item== None:   
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm)
                self.temp_item.setcor(self.temp_col)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append([x,y])
        elif self.status == 'translate' or self.status == 'rotate' or self.status == 'scale'  or self.status == 'clip':
            self.start_pos = [x,y] 
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    '''
    椭圆和直线都是给两个点，按下-移动-释放
    变换操作：按下-移动-释放
    '''
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.temp_item == None:
            pass
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status =='ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon' or self.status=='curve':
            self.temp_item.p_list[-1] = [x,y]
        elif self.status == 'translate':
            self.temp_item.p_list=alg.translate(self.plist,x-self.start_pos[0],y-self.start_pos[1])
        elif self.status == 'rotate':
            detax = x - self.start_pos[0]
            detay = y - self.start_pos[1]
            angle = 0
            if detax == 0:
                if  detay > 0:
                    angle = 90
                elif detay < 0:
                    angle = 270
            else:
                radangle = math.atan(detay/detax)
                angle = math.degrees(radangle)
            self.temp_item.p_list=alg.rotate(self.plist,self.start_pos[0],self.start_pos[1],angle)
        elif self.status == 'clip':
            self.temp_item.p_list=alg.clip(self.plist,self.start_pos[0],self.start_pos[1],x,y,self.temp_algorithm)
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    '''
   
    #直线,椭圆：按下鼠标后拖动绘制，松开绘制完成
    #多边形，曲线：鼠标取点，点击OK表示绘制完成
    缩放：按下鼠标选择中心点，滚轮选择放大还是缩小

    '''

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.finish_draw()
        elif self.status == 'polygon' or self.status == 'curve':
            self.temp_item.p_list[-1] = [x,y]
        elif self.status == 'translate':
            self.plist =self.temp_item.p_list
            self.finish_fluctuate()
        elif self.status == 'rotate':
            self.plist =self.temp_item.p_list
            self.finish_fluctuate()
        elif self.status == 'clip' :
            self.temp_item.p_list=alg.clip(self.plist,self.start_pos[0],self.start_pos[1],x,y,self.temp_algorithm)
            self.updateScene([self.sceneRect()])
            self.finish_fluctuate()
        self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)

    def wheelEvent (self, event):
        x = event.angleDelta().x()
        y = event.angleDelta().y()
        if self.status == 'scale' :
            if event.angleDelta().y() > 0:  #向上滚
                s = 1.2
            else:
                s = 0.8
            self.temp_item.p_list=alg.scale(self.plist,self.start_pos[0],self.start_pos[1],s)
            self.plist =self.temp_item.p_list
            self.finish_fluctuate()
        self.updateScene([self.sceneRect()])
class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.pencol = QColor(0,0,255)
    
    def setcor(self,col):
        self.pencol = col

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type =='':
            return
        item_pixels = None
        painter.setPen(self.pencol)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list,self.algorithm)
        for p in item_pixels:
                painter.drawPoint(*p)
        if self.selected:
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(self.boundingRect())

    #边界限制:曲线的边界限制是这个吗
    def boundingRect(self) -> QRectF:
        # if self.item_type == 'line':
        #     x0, y0 = self.p_list[0]
        #     x1, y1 = self.p_list[1]
        #     x = min(x0, x1)
        #     y = min(y0, y1)
        #     w = max(x0, x1) - x
        #     h = max(y0, y1) - y
        #     return QRectF(x - 1, y - 1, w + 2, h + 2)
        # elif self.item_type == 'polygon' or self.item_type == 'ellipse' or self.item_type == 'curve':
        #     x0 ,y0 = self.p_list[0]
        #     x1 = x0
        #     y1 = y0
        #     for i in range(len(self.p_list)):
        #         x,y = self.p_list[i]
        #         x0 = min(x0, x)
        #         y0 = min(y0, y)
        #         x1 = max(x1, x)
        #         y1 = max(y1, y)
        #     w = x1 - x0
        #     h = y1 - y0
        #     return QRectF(x0 - 1, y0 - 1, w + 2, h + 2)
        if self.p_list == None:
            return QRectF(0, 0, 0,0)
        x0 ,y0 = self.p_list[0]
        x1 = x0
        y1 = y0
        for i in range(len(self.p_list)):
            x,y = self.p_list[i]
            x0 = min(x0, x)
            y0 = min(y0, y)
            x1 = max(x1, x)
            y1 = max(y1, y)
        w = x1 - x0
        h = y1 - y0
        return QRectF(x0 - 1, y0 - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0
        self.w = 600
        self.h = 600
        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        save_canvas_act = file_menu.addAction('保存画布')
        exit_act = file_menu.addAction('退出')
        #------------------------
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        #---------------------------------
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act= edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')
        #----------------------------------
        ok_act = menubar.addAction('ok') #针对多边形，曲线
       
        

        # 连接信号和槽函数
        set_pen_act.triggered.connect(self.set_pen_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        save_canvas_act.triggered.connect(self.save_canvas_action)
        exit_act.triggered.connect(qApp.quit)
        #----------------------------
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        #------------------------
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        #--------------------------
        ellipse_act.triggered.connect(self.ellipse_action)
        #-------------------------------
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        #-------------------------------
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        #-------------------
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        #-------------
        ok_act.triggered.connect(self.ok_action)
       
        # self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
        self.list_widget.itemClicked.connect(self.canvas_widget.selection_changed)
       

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def inc_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id
    #画布操作------
    def set_pen_action(self):
        self.statusBar().showMessage('设置画笔')
        col = QColorDialog.getColor()
        if col.isValid():
            self.canvas_widget.update_corlor(col)
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    def reset_canvas_action(self):
        self.statusBar().showMessage('重置画布')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.canvas_widget.reset_canvas()
        self.item_cnt = 0
    def save_canvas_action(self):
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.statusBar().showMessage('保存画布')
        dialog=QFileDialog()
        filename=dialog.getSaveFileName(filter="Image Files(*.jpg *.png *.bmp)")
        if filename[0]:
            self.canvas_widget.save_canvas(filename[0], self.w, self.h)
    
    #------------
    def line_naive_action(self):
        self.statusBar().showMessage('Naive算法绘制线段')
        self.canvas_widget.start_draw_figure('Naive', str(self.item_cnt),'line')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    def line_dda_action(self):
        self.canvas_widget.start_draw_figure('DDA', str(self.item_cnt),'line')
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    def line_bresenham_action(self):
        self.canvas_widget.start_draw_figure('Bresenham', str(self.item_cnt),'line')
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.canvas_widget.start_draw_figure('DDA', str(self.item_cnt),'polygon') 
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_figure('Bresenham', str(self.item_cnt),'polygon')
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def ellipse_action(self):
        self.canvas_widget.start_draw_figure('none', str(self.item_cnt),'ellipse')
        self.statusBar().showMessage('中点画椭圆法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.canvas_widget.start_draw_figure('bezier', str(self.item_cnt),'curve')
        self.statusBar().showMessage('绘制贝塞尔曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_figure('b-spline', str(self.item_cnt),'curve')
        self.statusBar().showMessage('绘制三次b样条曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def ok_action(self):
        self.canvas_widget.finish_draw()
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    #---------------变换-----------------
    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移变换')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转变换')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    def  scale_action(self):
        self.canvas_widget.start_scale("scale")
        self.statusBar().showMessage('缩放变换')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip("Cohen-Sutherland")
        self.statusBar().showMessage('裁剪变换-cohen-sutherland')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    def clip_liang_barsky_action(self):
        self.canvas_widget.start_clip("Liang-Barsky")
        self.statusBar().showMessage('裁剪变换-liang-barsky')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
