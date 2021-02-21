import random, math
from Partition import *
from Room import Room

class BSP:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Partition_n(0, 0, self.width, self.height)
        self.corridors = []
        self.base = None

    def gen(self):
        self.generate()
        self.createRooms()
        self.createCorridors()

    def generate(self, partition=None):
        if partition == None:
            partition = self.root
        if partition.largeEnough():
            if partition.width/partition.height > 1.5:
                split = 0
            elif partition.height/partition.width > 1.5:
                split = 1
            else:
                split = random.randint(0,1)
            if split == 0:
                partition_end = partition.x + partition.width
                partition_split = random.randint(partition.x + math.floor(partition.width / 4), partition_end - math.floor(partition.width / 4))
                temp_width = partition_split - partition.x
                if temp_width < 250 and (temp_width/partition.height < 1.5 and partition.height/temp_width < 1.5):
                    temp_partition_1 = Partition_n(partition.x, partition.y, temp_width, partition.height, splitable=False)
                else:
                    temp_partition_1 = Partition_n(partition.x, partition.y, temp_width, partition.height)
                temp_width = partition_end - partition_split
                if temp_width < 250 and (temp_width/partition.height < 1.5 and partition.height/temp_width < 1.5):
                    temp_partition_2 = Partition_n(partition_split, partition.y, temp_width, partition.height, splitable=False)
                else:
                    temp_partition_2 = Partition_n(partition_split, partition.y, temp_width, partition.height)
            else:
                partition_end = partition.y + partition.height
                partition_split = random.randint(partition.y + math.floor(partition.height / 4), partition_end - math.floor(partition.height / 4))
                temp_height = partition_split - partition.y
                if temp_height < 250 and (temp_height/partition.width < 1.5 and partition.width/temp_height < 1.5):
                    temp_partition_1 = Partition_n(partition.x, partition.y, partition.width, temp_height, splitable=False)
                else:
                    temp_partition_1 = Partition_n(partition.x, partition.y, partition.width, temp_height)
                temp_height = partition_end - partition_split
                if temp_height < 250 and (temp_height/partition.width < 1.5 and partition.width/temp_height < 1.5):
                    temp_partition_2 = Partition_n(partition.x, partition_split, partition.width, temp_height, splitable=False)
                else:
                    temp_partition_2 = Partition_n(partition.x, partition_split, partition.width, temp_height)
            partition.setLeft(temp_partition_1)
            partition.setRight(temp_partition_2)
            if partition.left.splitable:
                self.generate(partition=partition.left)
            if partition.right.splitable:
                self.generate(partition=partition.right)

    def createRooms(self, partition=None):
        if partition == None:
            partition = self.root
        if partition.isLeaf():
            partition.createRoom()
        if partition.left != None:
            self.createRooms(partition.left)
        if partition.right != None:
            self.createRooms(partition.right)

    def createCorridors(self, partition=None):
        if partition == None:
            partition = self.root
        if partition.left != None and partition.right != None:
            self.corridors.append(Corridor(*partition.left.getCentre(), *partition.right.getCentre()))
        if partition.left != None:
            self.createCorridors(partition.left)
        if partition.right != None:
            self.createCorridors(partition.right)

    def getPartition(self, x, y, partition=None):
        if partition == None:
            partition = self.root
        if partition.hasRoom():
            self.base = partition
            print("Partition=", self.base.value())
            print("Room=", self.base.room.value())
            self.corridors = self.baseCorridors()
        elif not partition.largeEnough():
            print("Invalid Regeneration Location")
        elif partition.left.x == partition.right.x:
            if (partition.left.y + partition.left.height) > y:
                self.getPartition(x, y, partition=partition.left)
            else:
                self.getPartition(x, y, partition=partition.right)
        else:
            if (partition.left.x + partition.left.width) > x:
                self.getPartition(x, y, partition=partition.left)
            else:
                self.getPartition(x, y, partition=partition.right)

    def baseCorridors(self):
        temp_corridors = []
        for corridor in self.corridors:
            if corridor.start_y == corridor.end_y: #if horizontal
                if (corridor.start_y + 4) >= self.base.room.y and (corridor.start_y - 4) <= (self.base.room.y + self.base.room.height):
                    if not(corridor.start_x > (self.base.room.x + self.base.room.width) or corridor.end_x < self.base.room.x):
                        print("Corridor, s=",corridor.getStart(), "e=", corridor.getEnd())
                        temp_corridors.append(corridor)
            else:
                if (corridor.start_x + 4) >= self.base.room.x and (corridor.start_x - 4) <= (self.base.room.x + self.base.room.width):
                    if not(corridor.start_y > (self.base.room.y + self.base.room.height) or corridor.end_y < self.base.room.y):
                        print("Corridor, s=",corridor.getStart(), "e=", corridor.getEnd())
                        temp_corridors.append(corridor)
        return temp_corridors

    def regenerate(self):
        if self.base.x == 0 and self.base.y == 0:
            #top left corner
            return True
        elif (self.base.x + self.base.width) == self.width and self.base.y == 0:
            #top right corner
            return True
        elif (self.base.x + self.base.width) == self.width and (self.base.y + self.base.height) == self.height:
            #bottom right corner
            return True
        elif self.base.x == 0 and (self.base.y + self.base.height) == self.height:
            #bottom left corner
            return True
        elif self.base.y == 0:
            #joint to top screen bound
            return True
        elif (self.base.x + self.base.width) == self.width:
            #joint to right screen bound
            return True
        elif (self.base.y + self.base.height) == self.height:
            #joint to bottom screen bound
            return True
        elif self.base.x == 0:
            #joint to left screen bound
            return True
        else:
            #not on any bound
            return True
            