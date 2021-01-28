import random, math
from Partition import *

class BSP:
    def __init__(self, width, height, split_recursion):
        self.width = width
        self.height = height
        self.split_recursion = split_recursion

    def generate(self):
        partitions = []
        partitions.append(Partition_n(0, 0, self.width, self.height))

        for split in range(0, self.split_recursion):
            temp_partitions = []
            for partition in partitions:
                if partition.splitable:
                    if partition.width > partition.height * 1.5:
                        split = 0
                    elif partition.height > partition.width * 1.5:
                        split = 1
                    else:
                        split = random.randint(0,1) #0 is x-axis, 1 is y-axis
                    
                    if split == 0:
                        partition_start_x = partition.x
                        partition_end_x = partition.x + partition.width
                        partition_split = random.randint(partition_start_x + math.floor(partition.width / 4), partition_end_x - math.floor(partition.width / 4))
                        temp_w = partition_split - partition_start_x
                        if temp_w <= 250 and (temp_w < partition.height * 1.5 and temp_w * 1.5 > partition.height):
                            temp_partitions.append(Partition_n(partition_start_x, partition.y, temp_w, partition.height, splitable=False))
                        else:
                            temp_partitions.append(Partition_n(partition_start_x, partition.y, temp_w, partition.height))
                        temp_w = partition_end_x - partition_split
                        if temp_w <= 250 and (temp_w < partition.height * 1.5 and temp_w * 1.5 > partition.height):
                            temp_partitions.append(Partition_n((partition_split), partition.y, temp_w, partition.height, splitable=False))
                        else:
                            temp_partitions.append(Partition_n((partition_split), partition.y, temp_w, partition.height))
                    else:
                        partition_start_y = partition.y
                        partition_end_y = partition.y + partition.height
                        partition_split = random.randint(partition_start_y + math.floor(partition.height / 4), partition_end_y - math.floor(partition.height / 4))
                        temp_h = partition_split - partition_start_y
                        if temp_h <= 250 and (temp_h < partition.width * 1.5 and temp_h * 1.5 > partition.width):
                            temp_partitions.append(Partition_n(partition.x, partition.y, partition.width, temp_h, splitable=False))
                        else:
                            temp_partitions.append(Partition_n(partition.x, partition.y, partition.width, temp_h))
                        temp_h = partition_end_y - partition_split
                        if temp_h <= 250 and (temp_h < partition.width * 1.5 and temp_h * 1.5 > partition.width):
                           temp_partitions.append(Partition_n(partition.x, (partition_split), partition.width, temp_h, splitable=False))
                        else:
                            temp_partitions.append(Partition_n(partition.x, (partition_split), partition.width, temp_h))
                else:
                    temp_partitions.append(partition)
                #partition.splitable = False
            partitions.clear()
            for i in range(0, len(temp_partitions)):
                partitions.append(temp_partitions[i])
            temp_partitions.clear()
        return partitions
