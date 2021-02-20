import pygame, random
from BSP import BSP
from Room import Room

pygame.init()

SCREEN = (WIDTH, HEIGHT) = (1000, 700)

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

gameDisplay = pygame.display.set_mode(SCREEN)

pygame.display.set_caption("Dungeon Regeneration")

clock = pygame.time.Clock()

crashed = False

bsp = BSP(WIDTH, HEIGHT)
bsp.generate()
bsp.createRooms()
bsp.createCorridors()

def partitions(partition):
    if partition.left != None:
        partitions(partition.left)
    if partition.isLeaf():
        pygame.draw.rect(gameDisplay, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), partition.value())
    if partition.right != None:
        partitions(partition.right)

def corridors():
    for corridor in bsp.corridors:
        pygame.draw.line(gameDisplay, WHITE, corridor.getStart(), corridor.getEnd(), width=9)
        """
        if corridor.start_y == corridor.end_y: #if horizontal
            c1 = (corridor.start_x, corridor.start_y - 4)
            c2 = (corridor.end_x, corridor.end_y + 4)

        else:
            c1 = (corridor.start_x - 4, corridor.start_y)
            c2 = (corridor.end_x + 4, corridor.end_y)
        pygame.draw.circle(gameDisplay, BLACK, c1, 2)
        pygame.draw.circle(gameDisplay, BLACK, c2, 2)
        """


def rooms(partition):
    if partition.left != None:
        rooms(partition.left)
    if partition.isLeaf():
        pygame.draw.rect(gameDisplay, WHITE, partition.room.value())
    if partition.right != None:
        rooms(partition.right)

def drawDungeon():
    gameDisplay.fill(BLACK)
    partitions(bsp.root)
    corridors()
    rooms(bsp.root)
    #corridors(bsp.root)
            
drawDungeon()

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                bsp = BSP(WIDTH, HEIGHT)
                bsp.generate()
                bsp.createRooms()
                bsp.createCorridors()
                drawDungeon()
        elif event.type == pygame.MOUSEBUTTONUP:
            print("\nclick at", pygame.mouse.get_pos())
            bsp.getPartition(*pygame.mouse.get_pos())
            drawDungeon()
            #print(bsp.base)

    pygame.display.update()
    
    clock.tick(60)

pygame.quit()
quit()