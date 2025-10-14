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
import pygame, utils, math, controls

def move_player(screen_size: tuple, delta: float, player: dict):
	shape: pygame.Rect = player["shape"]
	pos_increment: int = int(player["speed"] * delta)
	
	if controls.is_pressed("right"):
		shape.x += pos_increment
	if controls.is_pressed("left"):
		shape.x -= pos_increment

	if not utils.is_rect_inside_screen(screen_size, shape):
		if shape.left < 0:
			shape.left = 0
		elif shape.right > screen_size[0]:
			shape.right = screen_size[0]
#end_def

def move_ball(screen_size: tuple, delta: float, ball: dict):
	shape: pygame.Rect = ball["shape"]

	shape.x += ball["speed"][0] * delta
	shape.y += ball["speed"][1] * delta

	if not utils.is_rect_inside_screen(screen_size, shape):
		if shape.left < 0 \
				or shape.right > screen_size[0]:
			ball["speed"][0] *= -1
			shape.x += ball["speed"][0] * delta
		elif shape.top < 0:
			ball["speed"][1] *= -1
			shape.y += ball["speed"][1] * delta
	#end_if
#end_def

def handle_ball_collisions(game_state: dict, game_objs: dict):
	ball: dict = game_objs["ball"]
	_handle_player_collision(ball, game_objs["player"])
	_handle_brick_collisions(game_state, ball, game_objs["bricks"])
#end_def

	
#end_def

def _handle_player_collision(ball: dict, player: dict):
	ball_shape: pygame.Rect = ball["shape"]
	player_shape: pygame.Rect = player["shape"]

	if ball_shape.colliderect(player_shape):
		# posição relativa do bola do centro do jogador
		# escala de -1 a 1 quanto a essa distancia
		hit_position: float = ball_shape.centerx - player_shape.centerx
		scale: float = hit_position / (float(player_shape.width) / 2)

		if scale > 1:
			scale = 1
		elif scale < -1:
			scale = -1

		interferenceX: float = 0.8

		length: float = pygame.Vector2.length(ball["speed"])

		ball["speed"][0] = length * scale * interferenceX
		ball["speed"][1] = math.sqrt(length**2 - ball["speed"][0]**2) * -1
#end_def

def _handle_brick_collisions(game_state: dict, ball: dict, bricks_obj: dict):
	ball_shape: pygame.Rect = ball["shape"]
	bricks: list = bricks_obj["list"]

	for brick in bricks:
		brick_shape: pygame.Rect = brick["shape"]
		
		if ball_shape.colliderect(brick_shape):
			# Quanto maior a velocidade
			# Maior a chance de error
			overlap_L: int = ball_shape.right - brick_shape.left
			overlap_R: int = brick_shape.right - ball_shape.left
			overlap_T: int = ball_shape.bottom - brick_shape.top
			overlap_B: int = brick_shape.bottom - ball_shape.top

			smallest = min(overlap_L, overlap_R, overlap_T, overlap_B)
			if smallest == overlap_L:
				ball["speed"][0] *= -1
				ball_shape.right = brick_shape.left - 1
			elif smallest == overlap_R:
				ball["speed"][0] *= -1
				ball_shape.left = brick_shape.right + 1
			elif smallest == overlap_T: 
				ball["speed"][1] *= -1
				ball_shape.bottom = brick_shape.top - 1
			else:  # Hit bottom
				ball["speed"][1] *= -1
				ball_shape.top = brick_shape.bottom + 1

			bricks.remove(brick)
			game_state["score"] += game_state["level"]
			break
		#end_if
	#end_for
#end_def
