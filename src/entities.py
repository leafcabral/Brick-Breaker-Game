"""
ASMbleia
	Ian Caliel Matos Cabral
	João Paulo Pipper da Silva
	Rafael Cabral Lopes
	Vitor Felberg Barcelos
Serra, Brasil
Recriação simples do jogo Brick Breaker em python utilizando a  biblioteca
pygame, usando como base o tutorial da Hashtag Programação, presente no link 
[https://www.youtube.com/watch?v=h0fKGPW_cxw]. Além da mudança das váriaveis
globais para escopo de função, modificando as funções, quando necessário, foram
feitos diversas mudanças para deixar o jogo e o código melhor em diversos
aspectos.
"""
import pygame
import utils

def new_player(screen_size: tuple) -> dict:
	size: tuple = (100, 20)
	# - 50 para padding da pontuacao
	position: tuple = (
		(screen_size[0] - size[0]) // 2,
		screen_size[1] - size[1] - 50
	)
	speed: float = 400

	return {
		"shape": pygame.Rect(position, size),
		"color": utils.get_main_color(),
		"speed": speed,
	}
#end_def

def new_ball(player: dict, radius: int = 10) -> dict:
	player_rect: pygame.Rect = player["shape"]
	circle: pygame.Rect = pygame.Rect(
		(player_rect.left, player_rect.top),
		(radius*2, radius*2)
	)
	circle.centerx = player_rect.centerx
	circle.centery = player_rect.centery - radius*2 - 10
	
	speed: int = player["speed"]

	ball: dict = {
		"shape": circle,
		"color": utils.get_main_color(),
		"radius": radius,
		"speed_original": [speed, -speed],
		"speed": [speed, -speed],
	}

	return ball
#end_def

def _new_brick(position: tuple, size: tuple, color: str) -> dict:
	return {
		"shape": pygame.Rect(position, size),
		"color": pygame.Color(color),
	}
#end_def

def create_bricks(screen_size: tuple, grid: tuple = (7, 4)) -> dict:
	spacing: int = 5
	padding: tuple = (70, 50)
	# azul, vermelho, amarelo, verde
	colors: tuple = ("dodgerblue", "firebrick", "gold3", "green4")

	brick_list: list = []

	# Blocos vao até 1/3 da altura da tela
	valid_area: pygame.Rect = pygame.Rect(
		padding,
		(screen_size[0] - padding[0]*2, screen_size[1]//3 - padding[1]),
	)
	size: tuple = (
		(valid_area.width // grid[0]) - spacing,
		(valid_area.height // grid[1]) - spacing,
	)

	increment: tuple = (spacing + size[0], spacing + size[1])
	pos: list = list(valid_area.topleft)

	for line in range(grid[1]):
		# Usa-se modulo para repetir a lista caso grid > lista
		color = colors[line % grid[1]]

		for column in range(grid[0]):
			brick_list.append(_new_brick(tuple(pos), size, color))

			pos[0] += increment[0]
		#end_for

		pos[0] = valid_area.left			
		pos[1] += increment[1]
	#end_for

	bricks: dict = {
		"list": brick_list,
		"grid": grid,
		"spacing": spacing,
		"padding": padding,
		"colors": colors,
	}
	return bricks
#end_def