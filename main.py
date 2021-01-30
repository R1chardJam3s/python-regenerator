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

def partitions(partition):
    if partition.left != None:
        partitions(partition.left)
    if partition.isLeaf():
        pygame.draw.rect(gameDisplay, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), partition.value())
    if partition.right != None:
        partitions(partition.right)

def corridors(partition):
    if partition.left != None and partition.right != None:
        #if partition.left.isLeaf() and partition.right.isLeaf():
        pygame.draw.line(gameDisplay, WHITE, partition.left.getCentre(), partition.right.getCentre(), width=10)
        if partition.left != None:
            corridors(partition.left)
        if partition.right != None:
            corridors(partition.right)

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
    corridors(bsp.root)
    rooms(bsp.root)
            
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
                drawDungeon()

    pygame.display.update()
    
    clock.tick(60)

pygame.quit()
quit()

