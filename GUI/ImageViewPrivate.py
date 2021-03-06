# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QRect,QSize

class ImageViewPrivate(QtGui.QWidget):
	def __init__(self,_p):
		QtGui.QWidget.__init__(self)
		self.setPalette(QtGui.QPalette(QtGui.QColor(128,128,128)))
		#self.setAttribute(Qt.WA_NoSystemBackground)
		#self.setAttribute(Qt.WA_OpaquePaintEvent)#Some weired effect?
		self.p = _p
		self.rb = None
		self.moveRb = False
		self.setMouseTracking(True)
	
	def cancelRect(self):
		'''Cancel selection rectangle'''
		if not self.rb: return
		self.rb.setGeometry(QRect(self.origin, QSize()))
		self.p.selRect(self.rb.geometry())
		
	def paintEvent(self,e):
		'''Handler called for repainting the widget,这个函数是自动调用的！'''
		x = self.width()
		y = self.height()
		pa = QtGui.QPainter(self)
		self.p.repaint(x,y,pa,e.rect())
		e.accept()
	
	def sizeHint(self):
		'''Return size hint from parent item'''
		return self.p.sizeHint()
	
	def mouseMoveEvent(self,e):
		
		if self.rb and (e.buttons() & Qt.LeftButton):
			r = QRect(self.origin,e.pos()).normalized()
			self.rb.setGeometry(r& self.p.data_rect)#use & to control the rb within the window
			self.p.selRect(self.rb.geometry())
			#print(self.rb.geometry())#检查rb的位置
		self.p.mouseCoordEvent(e)
		e.ignore()
		
	
	def mousePressEvent(self,e):
		if QtGui.QApplication.keyboardModifiers() == Qt.AltModifier and e.button() == Qt.LeftButton:
			region_grow_seed_point = e.pos()
			print("Region grow")
			self.p.selPoint(region_grow_seed_point)
			#parent.region_grow(region_grow_seed_point)
			e.accept()
			return
			
		if e.button() == Qt.LeftButton:
			self.moveRb = True
			self.origin = e.pos()
			if not self.rb: 
				self.rb = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle, self)
			self.rb.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
			self.rb.show()
			e.accept()
		else:
			e.ignore()
			
	def mouseReleaseEvent(self,e):
		if e.buttons() & Qt.LeftButton:#Left button is still pressed
			e.ignore() 
			return
		if self.moveRb:
			self.moveRb = False
			self.p.selRect(self.rb.geometry())
			self.p.rectCheck()
		else:
			e.ignore()