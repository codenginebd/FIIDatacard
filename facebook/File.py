class File:
	def __init__(self,fileName):
		self.fileName = fileName
	def OpenRead(self):
		self.file = open(self.fileName,'r')
	def OpenWrite(self):
		self.file = open(self.fileName,'w')
	def OpenAppend(self):
		self.file = open(self.fileName,'a')
	def Read(self):
		return self.file.read()
	def Write(self,contents):
		self.file.write(contents)
	def Close(self):
		self.file.close()