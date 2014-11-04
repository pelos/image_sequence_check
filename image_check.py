from PyQt4 import QtCore, QtGui
import sys
import argparse
import os
import OpenEXR
import re

#run the program as:
#image_check.py -file "folder/path/to/somewhere"

#todo: if the user don't input right path raise error
#todo if the user don't input right path print a help line with an example on how to do it.
#todo instead using an argument make a string in the UI where the user can choose the folder.

def parseOpt():
	"""
	parse the arguments from the command line
	"""
    parser = argparse.ArgumentParser(description="Check if the files in this folder are valid EXRs")
    parser.add_argument("-file", dest="filepath", help="The file path to be checked.")   
    return parser.parse_args()
ARGS = parseOpt()


class check_exr():
	"""
	class to do something with folder paths
	"""
	def __init__(self, path, start_frame = 98, end_frame= 102):
		self.path = path
		self.start_frame = start_frame
		self.end_frame = end_frame
		
		self.check_files(self.path)

	def check_files(self, directory):
	"""
	loop inside the files in the folders and check if the exr file is complete
	"""
		complete_exr = []
		fail_exr = []
		for root, dirs, files in os.walk(directory):
			file_name =  files[0]
			file_name = file_name.split(".")
			file_name = str(file_name[0:-3][0])

			list_of_posibles = [".", ".r.", ".l."]
						
			for j in list_of_posibles:
				for file in range(self.start_frame,self.end_frame+1):
					file_padding = str("%04d" %file)
					file = file_name+j+file_padding+".exr"
					if file == True:
					
						file_path = os.path.join(directory, file)
						print file_path
						print os.path.isfile(file_path)
						if file.endswith(".exr"):
							filepath = os.path.join(directory,file)
							try:
								im = OpenEXR.InputFile(filepath)
								valid = im.isComplete()
							except:
								valid = False
							
							if valid == False:	
								fail_exr.append(filepath)
							elif valid == True:
								complete_exr.append(filepath)
					if file == False:
						fail_exr.append(file)
		
		print "BAD EXRs"

		list_for_copy_paste = []
		list_left_eye = []
		list_right_eye = []	
		
		for i in fail_exr:
			frame_num =  i.split(".")[-2]
			list_for_copy_paste.append(frame_num)
		for i in fail_exr:
			if ".l." in i:
				list_left_eye.append(i.split(".")[-2])
			elif ".r." in i:
				list_right_eye.append(i.split(".")[-2])	
				
		list_for_copy_paste.sort()
		list_left_eye.sort()
		list_right_eye.sort()
			
		print "Bad Left"
		print re.sub('[set\[\[\]\'\(\) ]', "", str(list_left_eye)) 
		print "\n"
		print "Bad Right"
		print re.sub('[set\[\[\]\'\(\) ]', "", str(list_right_eye)) 
		print "\n"
		print "Bad Frames Right AND Left "
		print re.sub('[set\[\[\]\'\(\) ]', "", str(list_for_copy_paste)) 
		print "\n"*1
		set_for_copy_paste = str(set(list_for_copy_paste))
		print "condense right and left"	
		lf =  str(set_for_copy_paste)
		lff = re.sub('[set\[\[\]\'\(\) ]', "", lf)
		print lff
		IO.error(lff)


class CheckableDirModel(QtGui.QDirModel):
	"""
	a class to put check box on the folders inside a directory tree
	"""
	def __init__(self, parent=None):
		QtGui.QDirModel.__init__(self, None)
		self.checks = {}

	def data(self, index, role=QtCore.Qt.DisplayRole):
		if role != QtCore.Qt.CheckStateRole:
			return QtGui.QDirModel.data(self, index, role)
		else:
			if index.column() == 0:
				return self.checkState(index)

	def flags(self, index):
		return QtGui.QDirModel.flags(self, index) | QtCore.Qt.ItemIsUserCheckable

	def checkState(self, index):
		if index in self.checks:
			return self.checks[index]
		else:
			return QtCore.Qt.Unchecked

	def setData(self, index, value, role):
		if (role == QtCore.Qt.CheckStateRole and index.column() == 0):
			self.checks[index] = value
			self.emit(QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
			return True 

		return QtGui.QDirModel.setData(self, index, value, role)


class Ui_Dialog(QtGui.QDialog):
	"""
	UI of the program
	"""
	def __init__(self,parent=None):
		
		QtGui.QDialog.__init__(self,parent)
		self.setObjectName("Dialog")
		self.resize(600, 500)

		self.llayout = QtGui.QVBoxLayout(parent)

		self.model = CheckableDirModel()
		self.model.setFilter(QtCore.QDir.Dirs|QtCore.QDir.NoDotAndDotDot)

		self.tree = QtGui.QTreeView()
		self.tree.setModel(self.model)
		self.tree.setSortingEnabled(True)
		self.tree.setRootIndex(self.model.index(ARGS.filepath))

		self.tree.setWindowTitle("Dir View")
		self.tree.resize(400, 480)
		self.tree.setColumnWidth(0,200)
		
		self.but = QtGui.QPushButton(QtCore.QString("Run"))
		
		self.fs_line = QtGui.QLineEdit()
		self.fs_line.setText("Type the Start Frame here")

		self.fe_line = QtGui.QLineEdit()
		self.fe_line.setText("Type the End Frame here")
		
		self.llayout.addWidget(self.tree)
		
		self.llayout.addWidget(self.fs_line)
		self.llayout.addWidget(self.fe_line)
		self.llayout.addWidget(self.but)
		self.setLayout(self.llayout)
		
		self.but.clicked.connect(self.print_path)
		
	def print_path(self):
		for index,value in self.model.checks.items():
			try:
				if value.toBool():
					print self.model.filePath(index)
					path = check_exr( str(self.model.filePath(index)), int(self.fs_line.text()), int(self.fe_line.text())  )
				else:
					continue	
			except:
				print "Please select a Valid Range"


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())


