import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
import gamefuncs as gf

pygame.init()

clock = pygame.time.Clock()
delta: float = 0

screen: dict = gf.new_screen(width=600, height=600)
pygame.display.set_caption("Now Testing: Bricks")

player: dict = gf.new_player(screen["surface"].get_size())
ball: dict = gf.new_ball(player["shape"])
bricks: dict = gf.create_bricks(screen["surface"].get_size())

running: bool = True
brick_respawn_delay: float = 2
while running:
	screen["surface"].fill(screen["bg_color"])
	key_pressed = pygame.key.get_pressed()
	delta = clock.tick(60) / 1_000

	for event in pygame.event.get():
		if event.type == pygame.QUIT or key_pressed[pygame.K_ESCAPE]:
			running = False
	#end_for

	gf.move_player(screen, delta, player, key_pressed)
	gf.move_ball(screen, delta, ball)
	
	for i in bricks["list"]:
		pygame.draw.rect(screen["surface"], i["color"], i["shape"])

	if not bricks["list"]:
		if brick_respawn_delay <= 0:
			gf.reset_bricks(
				screen["surface"].get_size(),
				bricks
			)
		else:
			brick_respawn_delay -= delta

	pygame.display.flip()

pygame.quit()