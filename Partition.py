from Room import Room
import math
from Corridor import Corridor

class Partition:
    def __init__(self, x, y, width, height, splitable=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.splitable = splitable
        self.left = None
        self.right = None
        self.room = None

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

    def isLeaf(self):
        if self.isValid():
            if self.left == None and self.right == None:
                return True
            else:
                return False
        else:
            return False

    def value(self):
        return (self.x, self.y, self.width, self.height)

    def isValid(self):
        return (self.width > 75 and self.height > 75) and (self.width/self.height < 1.5 and self.height/self.width < 1.5)

    def getCentre(self):
        return (self.x + math.floor(self.width / 2), self.y + math.floor(self.height / 2))

    def largeEnough(self):
        return (self.width > 75 and self.height > 75)

    def createRoom(self):
        self.room = Room(self.x, self.y, self.width, self.height)

    def hasRoom(self):
        return (self.room != None)