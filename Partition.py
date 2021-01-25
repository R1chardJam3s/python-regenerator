class Partition:
    def __init__(self,x,y,width,height,splitable=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.splitable = splitable

    def value(self):
        return (self.x,self.y,self.width,self.height)
