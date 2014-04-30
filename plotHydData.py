#! /usr/bin/python

import sys
import csv
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

import rospy
from std_msgs.srv import Empty

#prepare datasets
data1=[]
data2=[]

#prepre GUI
app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Hydrophone data")

# read from csv
def readFile(fileName):
	print "Reading file", fileName
	i=0
	with open(fileName, 'rb') as csvfile:
		for row in csv.reader(csvfile):
			while i<len(row):
				if len(row[i]) == 0:
					break
#				print row[i]	#debug 
				if i%2:
					data1.append(int(row[i]))
				else:
					data2.append(int(row[i]))
				i=i+1


def plotData(data1, data2):
	print "Preparing GUI"

	win.resize(1000,750)
	win.setWindowTitle('data source: csv, data type: n(a,b)')

	# for pretty plots
	pg.setConfigOptions(antialias=True) 

	# first row
	hyd1 = win.addPlot(title="Hydrophone 1")
	hyd1.plot(data1, pen=(255,0,0))

	win.nextRow()
	# second row
	hyd2 = win.addPlot(title="Hydrophone 2")
	hyd2.plot(data2, pen=(0,0,255))

def graphPlotCallBack(req):
	fileName='./hydrophone_logged_data/No.3_0_deg.txt'
	readFile(fileName)
	plotData(data1,data2)
	return EmptyResponse()

'''
for i in sys.argv:
	if i!=sys.argv[0]:
		readFile(i)
		plotData(data1, data2)
'''

def plotServer():
	rospy.init_node('graph_plot_server')
	server = rospy.Service('graph_plot', Empty, graphPlotCallBack)
	print "Graph Plot Service ready"
    	r = rospy.Rate(10) # 10hz
    	while not rospy.is_shutdown():
    		rospy.spinOnce()
        	r.sleep()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
	try:
		 plotServer()
	except rospy.ROSInterruptException: pass
