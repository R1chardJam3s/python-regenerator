class Partition:
    def __init__(self, x, y, width, height, splitable=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.splitable = splitable

    def value(self):
        return (self.x, self.y, self.width, self.height)

    def isValid(self):
    	return (self.width > 75 and self.height > 75) and (self.width/self.height < 1.5 and self.height/self.width < 1.5)
