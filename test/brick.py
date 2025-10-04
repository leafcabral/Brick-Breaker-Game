import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
import gamefuncs as gf

pygame.init()

clock = pygame.time.Clock()
delta: float = 0

screen: dict = gf.new_screen(width=600, height=600)
pygame.display.set_caption("Now Testing: Bricks")

bricks: dict = gf.create_bricks(screen["surface"].get_size())

running: bool = True
time: float = 3
while running:
	screen["surface"].fill(screen["bg_color"])
	key_pressed = pygame.key.get_pressed()
	delta = clock.tick(60) / 1_000

	for event in pygame.event.get():
		if event.type == pygame.QUIT or key_pressed[pygame.K_ESCAPE]:
			running = False
	#end_for

	for i in bricks["list"]:
		pygame.draw.rect(screen["surface"], i["color"], i["shape"])

	if time > 0: 
		time -= delta
	else:
		if bricks["list"]:
			bricks["list"].pop()
		else:
			gf.reset_bricks(
				screen["surface"].get_size(),
				bricks
			)
			time = 3

	pygame.display.flip()

pygame.quit()