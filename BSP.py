import random, math
from Partition import *
from Room import Room

class BSP:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Partition(0, 0, self.width, self.height)
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
                    temp_partition_1 = Partition(partition.x, partition.y, temp_width, partition.height, splitable=False)
                else:
                    temp_partition_1 = Partition(partition.x, partition.y, temp_width, partition.height)
                temp_width = partition_end - partition_split
                if temp_width < 250 and (temp_width/partition.height < 1.5 and partition.height/temp_width < 1.5):
                    temp_partition_2 = Partition(partition_split, partition.y, temp_width, partition.height, splitable=False)
                else:
                    temp_partition_2 = Partition(partition_split, partition.y, temp_width, partition.height)
            else:
                partition_end = partition.y + partition.height
                partition_split = random.randint(partition.y + math.floor(partition.height / 4), partition_end - math.floor(partition.height / 4))
                temp_height = partition_split - partition.y
                if temp_height < 250 and (temp_height/partition.width < 1.5 and partition.width/temp_height < 1.5):
                    temp_partition_1 = Partition(partition.x, partition.y, partition.width, temp_height, splitable=False)
                else:
                    temp_partition_1 = Partition(partition.x, partition.y, partition.width, temp_height)
                temp_height = partition_end - partition_split
                if temp_height < 250 and (temp_height/partition.width < 1.5 and partition.width/temp_height < 1.5):
                    temp_partition_2 = Partition(partition.x, partition_split, partition.width, temp_height, splitable=False)
                else:
                    temp_partition_2 = Partition(partition.x, partition_split, partition.width, temp_height)
            partition.setLeft(temp_partition_1)
            partition.setRight(temp_partition_2)
            if partition.left.splitable:
                self.generate(partition=partition.left)
            if partition.right.splitable:
                self.generate(partition=partition.right)

    def createRooms(self, partition=None):
        if partition == None:
            partition = self.root
        if partition.isLeaf() and not (partition == self.base):
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
            return (True, partition)
        elif partition.left == None and partition.right == None:
            return (False, partition)
        elif partition.left.x == partition.right.x:
            if (partition.left.y + partition.left.height) > y:
                return self.getPartition(x, y, partition=partition.left)
            else:
                return self.getPartition(x, y, partition=partition.right)
        else:
            if (partition.left.x + partition.left.width) > x:
                return self.getPartition(x, y, partition=partition.left)
            else:
                return self.getPartition(x, y, partition=partition.right)

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

    def removeCorridors(self):
        rem = []
        for corridor in self.corridors:
            if corridor.start_y == corridor.end_y: #if horizontal
                if (corridor.start_y + 4) >= self.base.room.y and (corridor.start_y - 4) <= (self.base.room.y + self.base.room.height):
                    if not(corridor.start_x > (self.base.room.x + self.base.room.width) or corridor.end_x < self.base.room.x):
                        rem.append(corridor)
            else:
                if (corridor.start_x + 4) >= self.base.room.x and (corridor.start_x - 4) <= (self.base.room.x + self.base.room.width):
                    if not(corridor.start_y > (self.base.room.y + self.base.room.height) or corridor.end_y < self.base.room.y):
                        rem.append(corridor)
        for corridor in rem:
            self.corridors.remove(corridor)

    def rgc(self):
        self.createRooms()
        corridors = []
        for corridor in self.corridors:
            corridors.append(corridor)
        #check for room connectivity here
        cc = []
        for corridor in corridors:
            c1, c2 = [], []
            x, y = corridor.getStart()
            v, p = self.getPartition(x, y)
            if not v:
                #connect
                print("algorithm will connect (no room)", x, y)
                c1 = self.connect(x, y, v, p, corridor.start_y == corridor.end_y)
            else:
                if not p.room.contains(x, y):
                    print("algorithm will connect (room but no connectivity)", x, y, p == self.base)
                    c1 = self.connect(x, y, v, p, corridor.start_y == corridor.end_y)
            x, y = corridor.getEnd()
            v, p = self.getPartition(x, y)
            if p.room == None:
                #connect
                print("algorithm will connect (no room)", x, y)
                c2 = self.connect(x, y, v, p, corridor.start_y == corridor.end_y)
            else:
                if not p.room.contains(x, y):
                    print("algorithm will connect (room but no connectivity)", x, y, p == self.base)
                    c2 = self.connect(x, y, v, p, corridor.start_y == corridor.end_y)
            for c in c1:
                cc.append(c)
            for c in c2:
                cc.append(c)
        # /
        self.createCorridors()
        self.corridors = [*self.corridors, *cc]
        self.removeCorridors()
        for corridor in corridors:
            if corridor not in self.corridors:
                self.corridors.append(corridor)
        for corridor in self.corridors:
            index = self.corridors.index(corridor)
            for c in self.corridors:
                if corridor.getStart() == c.getStart() and corridor.getEnd() == c.getEnd():
                    if not index == self.corridors.index(c):
                        self.corridors.remove(c)
        
    def connect(self, x, y, v, p, cr_h):
        connectives = []
        cx, cy = 0, 0
        if v and (p != self.base):
            cx, cy = p.getCentre()
            #draw to centre
        else:
            # if p is base, or corridor is in a partition with no room
            if self.getPartition(p.getCentre()[0], p.y - 1)[0] and (self.getPartition(p.getCentre()[0], p.y - 1)[1] != self.base):
                np = self.getPartition(p.getCentre()[0], p.y - 1)[1]
                cx, cy = np.getCentre()
                #draw to centre
            elif self.getPartition(p.x + p.width + 1, p.y - 1)[0] and (self.getPartition(p.x + p.width + 1, p.y - 1)[1] != self.base):
                np = self.getPartition(p.x + p.width + 1, p.y - 1)[1]
                cx, cy = np.getCentre()
                #draw to centre
            elif self.getPartition(p.x + p.width + 1, p.getCentre()[1])[0] and (self.getPartition(p.x + p.width + 1, p.getCentre()[1])[1] != self.base):
                np = self.getPartition(p.x + p.width + 1, p.getCentre()[1])[1]
                cx, cy = np.getCentre()
                #draw to centre
            elif self.getPartition(p.x + p.width + 1, p.y + p.height + 1)[0] and (self.getPartition(p.x + p.width + 1, p.y + p.height + 1)[1] != self.base):
                np = self.getPartition(p.x + p.width + 1, p.y + p.height + 1)[1]
                cx, cy = np.getCentre()
                #draw to centre
            elif self.getPartition(p.getCentre()[0], p.y + p.height + 1)[0] and (self.getPartition(p.getCentre()[0], p.y + p.height + 1)[1] != self.base):
                np = self.getPartition(p.getCentre()[0], p.y + p.height + 1)[1]
                cx, cy = np.getCentre()
                #draw to centre
            elif self.getPartition(p.x - 1, p.y + p.height + 1)[0] and (self.getPartition(p.x - 1, p.y + p.height + 1)[1] != self.base):
                np = self.getPartition(p.x - 1, p.y + p.height + 1)[1]
                cx, cy = np.getCentre()
                #draw to centre
            elif self.getPartition(p.x - 1, p.getCentre()[1])[0] and (self.getPartition(p.x - 1, p.getCentre()[1])[1] != self.base):
                np = self.getPartition(p.x - 1, p.getCentre()[1])[1]
                cx, cy = np.getCentre()
                #draw to centre
            elif self.getPartition(p.x - 1, p.y - 1)[0] and (self.getPartition(p.x - 1, p.y - 1)[1] != self.base):
                np = self.getPartition(p.x - 1, p.y - 1)[1]
                cx, cy = np.getCentre()
                #draw to centre
            else:
                count = 0
                while count < 20:
                    if cr_h:
                        cx = x
                        cy = random.randint(0, self.height)
                    else:
                        cx = random.randint(0, self.width)
                        cy = y
                    if self.getPartition(cx, cy)[0]:
                        if self.getPartition(cx, cy)[1].room.contains(cx, cy) and self.getPartition(cx, cy)[1] != self.base:
                            break
                    count += 1
                if count == 20:
                    while True:
                        cx = random.randint(0, self.width)
                        cy = random.randint(0, self.height)
                        if self.getPartition(cx, cy)[0]:
                            if self.getPartition(cx, cy)[1].room.contains(cx, cy) and self.getPartition(cx, cy)[1] != self.base:
                                break
                #check partition, and draw
        if cr_h:
            # existing corridor is horizontal
            c1 = Corridor(x, y, x, cy)
            connectives.append(c1)
            if self.getPartition(x, cy)[0]:
                if not self.getPartition(x, cy)[1].room.contains(x, cy):
                    c2 = Corridor(x, cy, cx, cy)
                    connectives.append(c2)
            else:
                c2 = Corridor(x, cy, cx, cy)
                connectives.append(c2)
        else:
            # existing corridor is vertical
            c1 = Corridor(x, y, cx, y)
            connectives.append(c1)
            if self.getPartition(cx, y)[0]:
                if not self.getPartition(cx, y)[1].room.contains(cx, y):
                    c2 = Corridor(cx, y, cx, cy)
                    connectives.append(c2)
            else:
                c2 = Corridor(cx, y, cx, cy)
                connectives.append(c2)
        print("connect to=", cx, cy)
        return connectives

    def regenerate(self, x, y):
        p = self.getPartition(x, y)
        if not p[0]:
            print("Invalid Regeneration Location")
        else:
            self.base = p[1]
            print("Partition=", self.base.value())
            print("Room=", self.base.room.value())
            self.corridors = self.baseCorridors()
            if self.base.x == 0 and self.base.y == 0:
                #top left corner
                temp_root = Partition(0, 0, self.width, self.height)
                root_l = Partition(0, 0, self.base.width, self.height)
                root_r = Partition(self.base.width, 0, (self.width - self.base.width), self.height)
                temp_root.setLeft(root_l)
                temp_root.setRight(root_r)
                self.generate(root_r)
                root_l.setLeft(self.base)
                root_l.setRight(Partition(0, self.base.height, self.base.width, (self.height - self.base.height)))
                self.generate(root_l.right)
                self.root = temp_root
                self.rgc()
                #checking that corridor meets a room isn't implemented
            elif (self.base.x + self.base.width) == self.width and self.base.y == 0:
                #top right corner
                temp_root = Partition(0, 0, self.width, self.height)
                root_l = Partition(0, 0, (self.width - self.base.width), self.height)
                root_r = Partition(self.base.x, self.base.y, self.base.width, self.height)
                temp_root.setLeft(root_l)
                temp_root.setRight(root_r)
                self.generate(root_l)
                root_r.setLeft(self.base)
                root_r.setRight(Partition(self.base.x, self.base.height, self.base.width, (self.height - self.base.height)))
                self.generate(root_r.right)
                self.root = temp_root
                self.rgc()
            elif (self.base.x + self.base.width) == self.width and (self.base.y + self.base.height) == self.height:
                #bottom right corner
                temp_root = Partition(0, 0, self.width, self.height)
                root_l = Partition(0, 0, (self.width - self.base.width), self.height)
                root_r = Partition(self.base.x, 0, self.base.width, self.height)
                temp_root.setLeft(root_l)
                temp_root.setRight(root_r)
                self.generate(root_l)
                root_r.setLeft(Partition(self.base.x, 0, self.base.width, (self.height - self.base.height)))
                root_r.setRight(self.base)
                self.generate(root_r.left)
                self.root = temp_root
                self.rgc()
            elif self.base.x == 0 and (self.base.y + self.base.height) == self.height:
                #bottom left corner
                temp_root = Partition(0, 0, self.width, self.height)
                root_l = Partition(0, 0, self.base.width, self.height)
                root_r = Partition(self.base.width, 0, (self.width - self.base.width), self.height)
                temp_root.setLeft(root_l)
                temp_root.setRight(root_r)
                self.generate(root_r)
                root_l.setLeft(Partition(0, 0, self.base.width, (self.height - self.base.height)))
                root_l.setRight(self.base)
                self.generate(root_l.left)
                self.root = temp_root
                self.rgc()
            elif self.base.y == 0:
                #joint to top screen bound
                temp_root = Partition(0, 0, self.width, self.height)
                root_l = Partition(0, 0, self.width, self.base.height)
                root_r = Partition(0, self.base.height, self.width, (self.height - self.base.height))
                temp_root.setLeft(root_l)
                temp_root.setRight(root_r)
                self.generate(root_r)
                root_l.setLeft(Partition(0, 0, self.base.x, self.base.height))
                root_l_r = Partition(self.base.x, self.base.y, (self.width - self.base.x), self.base.height)
                root_l.setRight(root_l_r)
                self.generate(root_l.left)
                root_l_r.setLeft(self.base)
                root_l_r.setRight(Partition((self.base.x + self.base.width), 0, (self.width - (self.base.x + self.base.width)), self.base.height))
                self.generate(root_l_r.right)
                self.root = temp_root
                self.rgc()
            elif (self.base.x + self.base.width) == self.width:
                #joint to right screen bound
                temp_root = Partition(0, 0, self.width, self.height)
                root_l = Partition(0, 0, (self.width - self.base.width), self.height)
                root_r = Partition(self.base.x, 0, self.base.width, self.height)
                temp_root.setLeft(root_l)
                temp_root.setRight(root_r)
                self.generate(root_l)
                root_r.setLeft(Partition(self.base.x, 0, self.base.width, self.base.y))
                root_r_r = Partition(self.base.x, self.base.y, self.base.width, (self.height - self.base.y))
                root_r.setRight(root_r_r)
                self.generate(root_r.left)
                root_r_r.setLeft(self.base)
                root_r_r.setRight(Partition(self.base.x, (self.base.y + self.base.height), self.base.width, (self.height - (self.base.y + self.base.height))))
                self.generate(root_r_r.right)
                self.root = temp_root
                self.rgc()
            elif (self.base.y + self.base.height) == self.height:
                #joint to bottom screen bound
                temp_root = Partition(0, 0, self.width, self.height)
                root_l = Partition(0, 0, self.width, self.base.y)
                root_r = Partition(0, self.base.y, self.width, self.base.height)
                temp_root.setLeft(root_l)
                temp_root.setRight(root_r)
                self.generate(root_l)
                root_r.setLeft(Partition(0, self.base.y, self.base.x, self.base.height))
                root_r_r = Partition(self.base.x, self.base.y, (self.width - self.base.x), self.base.height)
                root_r.setRight(root_r_r)
                self.generate(root_r.left)
                root_r_r.setLeft(self.base)
                root_r_r.setRight(Partition((self.base.x + self.base.width), self.base.y, (self.width - (self.base.x + self.base.width)), self.base.height))
                self.generate(root_r_r.right)
                self.root = temp_root
                self.rgc()
            elif self.base.x == 0:
                #joint to left screen bound
                temp_root = Partition(0, 0, self.width, self.height)
                root_l = Partition(0, 0, self.base.width, self.height)
                root_r = Partition(self.base.width, 0, (self.width - self.base.width), self.height)
                temp_root.setLeft(root_l)
                temp_root.setRight(root_r)
                self.generate(root_r)
                root_l.setLeft(Partition(0, 0, self.base.width, self.base.y))
                root_l_r = Partition(self.base.x, self.base.y, self.base.width, (self.height - self.base.y))
                root_l.setRight(root_l_r)
                self.generate(root_l.left)
                root_l_r.setLeft(self.base)
                root_l_r.setRight(Partition(0, (self.base.y + self.base.height), self.base.width, (self.height - (self.base.y + self.base.height))))
                self.generate(root_l_r.right)
                self.root = temp_root
                self.rgc()
            else:
                #not on any bound
                temp_root = Partition(0, 0, self.width, self.height)
                root_l = Partition(0, 0, self.base.x, self.height)
                root_r = Partition(self.base.x, 0, (self.width - self.base.x), self.height)
                temp_root.setLeft(root_l)
                temp_root.setRight(root_r)
                self.generate(root_l)
                root_r_l = Partition(self.base.x, 0, self.base.width, self.height)
                root_r_r = Partition((self.base.x + self.base.width), 0, (self.width - (self.base.x + self.base.width)), self.height)
                root_r.setLeft(root_r_l)
                root_r.setRight(root_r_r)
                self.generate(root_r_r)
                root_r_l_l = Partition(self.base.x, 0, self.base.width, self.base.y)
                root_r_l_r = Partition(self.base.x, self.base.y, self.base.width, (self.height - self.base.y))
                root_r_l.setLeft(root_r_l_l)
                root_r_l.setRight(root_r_l_r)
                self.generate(root_r_l_l)
                root_r_l_r.setLeft(self.base)
                root_r_l_r.setRight(Partition(self.base.x, (self.base.y + self.base.height), self.base.width, (self.height - (self.base.y + self.base.height))))
                self.generate(root_r_l_r.right)
                self.root = temp_root
                self.rgc()