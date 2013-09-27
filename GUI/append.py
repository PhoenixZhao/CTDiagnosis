from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QRect

def getDir(fd):
	'''Get current directory from File Dialog'''
	d=fd.directory();
	return d.absolutePath()

def openFileDialog(parent,caption,settingName,filters,savePath):
	global globalSettings
	fd = QtGui.QFileDialog(parent)
	#if filters.size():#AttributeError: 'QStringList' object has no attribute 'size'
	if filters.count():
		#Set filters if filters specified
		fd.setFilters(filters)
	if  not caption.isNull():
		fd.setWindowTitle(caption)
	if savePath.isNull():
	        #No save path specified -> start in current directory
		fd.setDirectory(".")
        else:
		#Try to set last used saved path, if it exists
		globalSettings = QtCore.QSettings("JiZhe","CTAnalysis")
		fd.setDirectory(globalSettings.value("history/path/"+savePath,"."))
	fd.setFileMode(QtGui.QFileDialog.ExistingFile)
	while True:
		if  not settingName.isNull():
			#// Restore window position from settings if applicable
			globalSettings = QtCore.QSettings("JiZhe","CTAnalysis")
			globalSettings.restoreWindow(fd,settingName)
		if fd.exec_()==QtGui.QDialog.Accepted:
			if  not settingName.isNull():
				#Save window position to settings if applicable
				globalSettings.saveWindow(fd,settingName)
			if not savePath.isNull():
				#Save the path if desired
				if globalSettings.read("history/save_filePath"):
					#//Note that there is only one central setting "save paths in dialog" for all dialog types
					globalSettings.write("history/path/"+savePath,getDir(fd));
			files = fd.selectedFiles()
			if  not files.isEmpty(): name = files[0]
			if  QtCore.QFileInfo(name).isDir():#directory was selected
				#** \todo  test this ! */ 
				fd.setDirectory(name)
				continue#restart dialog
			return name
		return QtCore.QString()