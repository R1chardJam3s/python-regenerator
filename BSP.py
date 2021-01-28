import random, math
from Partition import *

class BSP:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Partition_n(0, 0, self.width, self.height)

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