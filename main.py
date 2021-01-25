import pygame, random
from BSP import BSP

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

bsp = BSP(WIDTH, HEIGHT, 6)
partitions = bsp.generate()

def drawDungeon():
    gameDisplay.fill(BLACK)
    for partition in partitions:
        if partition.isValid():
            pygame.draw.rect(gameDisplay, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                             partition.value())

drawDungeon()

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                partitions = bsp.generate()
                drawDungeon()

    pygame.display.update()
    
    clock.tick(60)

pygame.quit()
quit()

