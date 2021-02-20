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
        #print("run")
        if partition == None:
            partition = self.root
        if partition.hasRoom():
            #print(partition.hasRoom(), partition.isLeaf(), partition.value())
            #print(partition)
            self.base = partition
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
            if corridor.start_y == corridor.end_y:
                if (corridor.start_y + 4) >= self.base.room.y and (corridor.start_y - 4) <= (self.base.room.y + self.base.room.width):
                    if corridor.start_x >= self.base.room.x and corridor.start_x <= (self.base.room.x + self.base.room.width):
                        print("Corridor",corridor.getStart(), corridor.getEnd(),"is a base corridor")
                        temp_corridors.append(corridor)
                    elif corridor.end_x >= self.base.room.x and corridor.end_x <= (self.base.room.x + self.base.room.width):
                        print("Corridor",corridor.getStart(), corridor.getEnd(),"is a base corridor")
                        temp_corridors.append(corridor)
                    elif self.base.room.x > corridor.start_x and self.base.room.x < corridor.end_x:
                        print("Corridor",corridor.getStart(), corridor.getEnd(),"is a base corridor")
                        temp_corridors.append(corridor)
            else:
                if (corridor.start_x + 4) >= self.base.room.x and (corridor.start_x - 4) <= (self.base.room.x + self.base.room.height):
                    if corridor.start_y >= self.base.room.y and corridor.start_y <= (self.base.room.y + self.base.room.height):
                        print("Corridor",corridor.getStart(), corridor.getEnd(),"is a base corridor")
                        temp_corridors.append(corridor)
                    elif corridor.end_y >= self.base.room.y and corridor.end_y <= (self.base.room.y + self.base.room.height):
                        print("Corridor",corridor.getStart(), corridor.getEnd(),"is a base corridor")
                        temp_corridors.append(corridor)
                    elif self.base.room.y > corridor.start_y and self.base.room.y < corridor.end_y:
                        print("Corridor",corridor.getStart(), corridor.getEnd(),"is a base corridor")
                        temp_corridors.append(corridor)
        return temp_corridors

    def baseCorridors_new(self):
        temp_corridors = []
        r1 = (self.base.room.x, self.base.room.y)
        r2 = (self.base.room.x + self.base.room.width, self.base.room.y + self.base.room.height)
        print(r1,r2)
        for corridor in self.corridors:
            if corridor.start_y == corridor.end_y: #if horizontal
                c1 = (corridor.start_x, corridor.start_y - 4)
                c2 = (corridor.end_x, corridor.end_y + 4)

                if self.overlap(*r1, *r2, *c1, *c2):
                    print("true")
                    temp_corridors.append(corridor)
            else:
                c1 = (corridor.start_x - 4, corridor.start_y)
                c2 = (corridor.end_x + 4, corridor.end_y)

                if self.overlap(*r1, *r2, *c1, *c2):
                    print("true")
                    temp_corridors.append(corridor)

        return temp_corridors

    #algorithm based on geeksforgeeks article: find two retangles overlap
    def overlap(self, r1_x, r1_y, r2_x, r2_y, c1_x, c1_y, c2_x, c2_y):
        if r1_x >= c2_x or c1_x >= r2_x:
            return False

        if r1_y <= c2_y or c1_y <= r2_y:
            return False

        return True