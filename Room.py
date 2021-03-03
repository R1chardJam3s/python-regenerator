import random, math

class Room:

	def __init__(self, x, y, w, h):
		self.width = w - random.randint(10, math.floor(w / 2))
		self.height = h - random.randint(10, math.floor(h / 2))
		self.x = random.randint(x + 5, (x + w - 5) - self.width)
		self.y = random.randint(y + 5, (y + h - 5) - self.height)

	def value(self):
		return (self.x, self.y, self.width, self.height)

	def contains(self, x, y):
		return (x >= self.x) and (x <= self.x + self.width) and (y >= self.y) and (y <= self.y + self.height)