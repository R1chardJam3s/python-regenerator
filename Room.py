import random, math

class Room:

	def __init__(self, x, y, w, h):
		self.width = w - random.randint(5, math.floor(w / 2))
		self.height = h - random.randint(5, math.floor(h / 2))
		self.x = random.randint(x, (x + w) - self.width)
		self.y = random.randint(y, (y + h) - self.height)

	def value(self):
		return (self.x, self.y, self.width, self.height)