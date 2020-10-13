# -*- coding: utf-8 -*-
from PyQt5 import QtCore
import cv2
import sqlite3
import os
import sys
from PIL import Image
import PythonMagick
import shutil
import os
import time

class MyThread(QtCore.QThread):  
	def __init__(self):  
		super(MyThread,self).__init__()

	singal_text = QtCore.pyqtSignal(str,int,str)
	
	def check_fps(self,path,width,height):
		img = Image.open(path)
		imgSize = img.size
		he = imgSize[1]
		wi = imgSize[0]
		if wi == width and he == height:
			return True
		else:
			return False
	
	def load_img_list(self,path):
		filelist = []
		incorrect = []
		mask = True
		path_img = os.getcwd() + '\\img-' + str(int(time.time()))  #复制图片至img目录下
		shutil.copytree(path,path_img)
		filelist = os.listdir(path_img)
		lenght = len(filelist)
		for m in filelist:
			if m.endswith('.jpg') == False:
				mask = False
				break
		if mask == True:
			for i in range(lenght):
				filelist[i] = path_img + '\\' + str(i + 1) + '.jpg'
		else:
			return incorrect
		return filelist
	
	def run(self):
		try:
			e_0 = '图片预加载完毕'
			e_1 = '图片预加载失败'
			e_2 = '分辨率检查完毕，分辨率正确'
			e_3 = '分辨率检查中止，分辨率出现错误，错误文件为：'
			e_4 = 'avi生成完毕，保存位置为：'
			e_5 = 'avi生成失败'
			e_6 = '其他未知错误'
			filelist = []
			path = ''
			savepath = ''
			fps = 0
			width = 0
			height = 0
			list2str = ''
			conn=sqlite3.connect('prc2avi.sqlite')
			cur=conn.cursor()
			cursor = cur.execute("SELECT path,savepath,fps,width,height from msg")
			tag = 1
			for row in cursor:
				path = row[0]
				savepath = row[1]
				fps = row[2]
				width = row[3]
				height = row[4]
			cur.execute("DELETE from msg;")
			conn.commit()
			conn.close()
			filelist = self.load_img_list(path)
			if len(filelist) != 0:
				for i in range(len(filelist)):
					list2str = list2str + filelist[i] + ';'
				self.singal_text.emit(list2str,0,e_0)
				for m in range(len(filelist)):
					flag = self.check_fps(filelist[m],width,height)
					if flag == False:
						img = PythonMagick.Image(filelist[m])
						xm = str(width) + 'x' + str(height)
						img.sample(xm)
						img.write(filelist[m])
						print(filelist[m] + xm)
						e_8 = str(filelist[m]) + '分辨率错误，执行修改中！'
						self.singal_text.emit('incorrect',8,e_8)
						
						continue
				if tag == 1:
					self.singal_text.emit('ok',2,e_2)
					try:
						size = (width,height)
						fourcc = cv2.VideoWriter_fourcc('I','4','2','0')
						video = cv2.VideoWriter(savepath,fourcc,fps,size)
						for item in filelist:
							img = cv2.imread(item)
							video.write(img)
							e_7 = item + '写入完成!'
							self.singal_text.emit('ok',7,e_7)
						e_4 = e_4 + savepath
						video.release()
						cv2.destroyAllWindows()
						self.singal_text.emit('ok',4,e_4)
					except:
						self.singal_text.emit('incorrect',5,e_5)
				else:
					self.singal_text.emit('incorrect',3,e_3)
			else:
				self.singal_text.emit('incorrect',1,e_1)
		except:
			print(sys.exc_info())
			self.singal_text.emit('incorrect',6,e_6)
		