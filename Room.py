from Partition import Partition

class Room:
	def __init__(self, partition):
		self.partition = partition
		self.x,self.y,self.width,self.height = generate()

	def generate():
		x = self.partition.x
		y = self.partition.y
		width = self.partition.width
		height = self.partition.height
		return x,y,width,height