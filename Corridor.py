class Corridor:
	def __init__(self, start_x, start_y, end_x, end_y):
		self.start_x = start_x
		self.start_y = start_y
		self.end_x = end_x
		self.end_y = end_y

	def getStart(self):
		return(self.start_x, self.start_y)

	def getEnd(self):
		return(self.end_x, self.end_y)