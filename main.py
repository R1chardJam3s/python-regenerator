import pygame, random
from BSP import BSP

pygame.init()

SCREEN = (WIDTH, HEIGHT) = (1000, 700)

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

gameDisplay = pygame.display.set_mode(SCREEN)
gameDisplay.fill(BLACK)
pygame.display.set_caption("Dungeon Regeneration")

clock = pygame.time.Clock()

crashed = False

bsp = BSP(WIDTH, HEIGHT, 10)
partitions = bsp.generate()

for partition in partitions:
        pygame.draw.rect(gameDisplay, (random.randint(0,255),random.randint(0,255), random.randint(0,255)),
                         partition.value())

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                gameDisplay.fill(BLACK)
                partitions = bsp.generate()
                for partition in partitions:
                    pygame.draw.rect(gameDisplay, (random.randint(0,255),random.randint(0,255), random.randint(0,255)),
                                     partition.value())

    pygame.display.update()
    
    clock.tick(60)

pygame.quit()
quit()
