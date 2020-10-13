 # -*- coding: utf-8 -*
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
import main
import time
from PyQt5 import QtCore
import mythread
import sqlite3


class MainCode(QMainWindow,main.Ui_MainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		main.Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.loadImg)   #加载图片文件夹路径控件连接动作函数
		self.pushButton_2.clicked.connect(self.saveAvi)       #生成avi保存文件位置控件槽函数
		self.pushButton_3.clicked.connect(self.startCreate)      #开始生成控件槽函数
		
	def loadImg(self):
		path = QFileDialog.getExistingDirectory(self, "请选择加载图片文件夹路径", "D:\\")
		loadPath_msg = '定义图片加载路径: ' + path
		self.lineEdit_3.setText(path)
		self.textBrowser.append(loadPath_msg)
		
	def saveAvi(self):
		path = QFileDialog.getExistingDirectory(self, "请选择avi文件保存文件夹路径", "D:\\")
		filename = '/test-' + str(int(time.time())) + '.avi'
		loadPath_msg = '定义保存avi文件路径: ' + path + filename
		self.lineEdit_4.setText(path + filename)
		self.textBrowser.append(loadPath_msg)
		
	def startCreate(self):
		self.thread = mythread.MyThread()
		self.thread.singal_text.connect(self.thread_start)
		conn=sqlite3.connect('prc2avi.sqlite')
		cur=conn.cursor()
		cur.execute('create table if not exists msg(path text,savepath text,fps int,width int,height int);')
		cur.execute('insert into msg(path,savepath,fps,width,height) values(\'' + self.lineEdit_3.text() + '\',\'' + self.lineEdit_4.text() + '\',' + str(self.lineEdit_5.text()) + ',' + str(self.lineEdit.text()) + ',' + str(self.lineEdit_2.text()) + ')')
		conn.commit()
		cur.close()
		conn.close()
		self.thread.start()
		
	def thread_start(self,loadfile,id,e):
		if id == 0:
			filelist = loadfile.split(';')
			for item in range(len(filelist)):
				self.textBrowser_2.append(filelist[item] + '预加载成功')
			self.textBrowser.append(e)
		if id == 1:
			self.textBrowser.append(e + '，请检查图片是否存在')
		if id == 2:
			self.textBrowser.append(e)
		if id == 3:
			self.textBrowser.append(e)
		if id == 4:
			self.textBrowser.append(e)
		if id == 5:
			self.textBrowser.append(e)
		if id == 6:
			self.textBrowser.append(e)
		if id == 7:
			self.textBrowser.append(e)
		if id == 8:
			self.textBrowser.append(e)
	
		
if __name__=='__main__':
	app = QApplication(sys.argv)
	md = MainCode()
	md.show()
	sys.exit(app.exec_())