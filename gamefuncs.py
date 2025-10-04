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

def new_screen(
		width: int = 600,
		height: int = 600,
		bg_color: str = "black") -> dict:
	surface = pygame.display.set_mode((width, height))
	screen: dict = {
		"surface": surface,
		"rect": surface.get_rect(),
		"bg_color": pygame.Color(bg_color),
	}

	return screen
#end_def

def new_player(
		position: tuple,
		size: tuple = (100, 20),
		color: str = "white",
		speed: float = 400) -> dict:
	return {
		"shape": pygame.Rect(position, size),
		"color": pygame.Color(color),
		"speed": speed,
	}
#end_def

def new_ball(
		player: pygame.Rect,
		radius: float = 10,
		color: str = "white",
		speed: list = [300, -300],
		offset_x: int = 0,
		offset_y: int = 0) -> dict:
	topLeftCorner: tuple = (
		player.centerx - radius + offset_x,
		player.centery - radius + offset_y
	)
	diameter: float = radius*2

	ball: dict = {
		"shape": pygame.Rect(topLeftCorner, (diameter, diameter)),
		"color": pygame.Color(color),
		"offset_x": offset_x,
		"offset_y": offset_y,
		"speed_original": speed.copy(),
		"speed": speed,
	}

	return ball
#end_def

def new_brick(position: list, size: tuple, color: str) -> dict:
	return {
		"shape": pygame.Rect(position, size),
		"color": pygame.Color(color),
	}
#end_def

def create_bricks(
		screen_size: tuple,
		grid: tuple = (7, 4),
		spacing: int = 5,
		padding: tuple = (70, 50),
		colors: list = [
			"dodgerblue", # blue
			"firebrick", # red
			"gold3", # yellow
			"green4" # green
		]
		) -> dict:
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
			brick_list.append(new_brick(pos, size, color))

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

def is_rect_inside_screen(screen: dict, rect: pygame.Rect) -> bool:
	return screen["rect"].contains(rect)
#end_def

def clamp_rect_to_screen(screen: dict, rect: pygame.Rect):
	rect.clamp_ip(screen["rect"])
#end_def

def move_player(screen: dict, delta: float, player: dict, keys):
	shape: pygame.Rect = player["shape"]
	pos_increment: int = int(player["speed"] * delta)
	
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		shape.x += pos_increment
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		shape.x -= pos_increment

	if not is_rect_inside_screen(screen, shape):
		clamp_rect_to_screen(screen, shape)
#end_def

def move_ball(screen: dict, delta: float, ball: dict):
	shape: pygame.Rect = ball["shape"]
	screen_rect: pygame.Rect = screen["rect"]

	shape.x += ball["speed"][0] * delta
	shape.y += ball["speed"][1] * delta

	if not is_rect_inside_screen(screen, shape):
		if shape.left < screen_rect.left \
				or shape.right > screen_rect.right:
			ball["speed"][0] *= -1
		elif shape.top < screen_rect.top:
			ball["speed"][1] *= -1
		
		clamp_rect_to_screen(screen, shape)
	#end_if
#end_def

def handle_ball_collisions(game_state: dict, ball: dict, game_objs: dict):
	ball_shape: pygame.Rect = ball["shape"]
	player_shape: pygame.Rect = game_objs["player"]["shape"]
	bricks: list = game_objs["bricks"]

	if ball_shape.colliderect(player_shape):
		# posição relativa do bola do centro do jogador
		# escala de -1 a 1 quanto a essa distancia
		hit_position: int = ball_shape.centerx - player_shape.centerx
		scale: float = hit_position // (player_shape.width / 2)

		ball["speed"][0] = ball["speed_original"][0] * scale
		ball["speed"][1] *= -1
		
		#ball_shape.bottom = player_shape.bottom
	else:
		for brick in bricks.copy():
			brick_shape: pygame.Rect = brick["shape"]

			if ball_shape.colliderect(brick_shape):
				# Quanto maior a velocidade
				# Maior a chance de error
				overlap_L: int = ball_shape.right - brick_shape.left
				overlap_R: int = brick_shape.right - ball_shape.left
				overlap_T: int = ball_shape.bottom - brick_shape.top
				overlap_B: int = brick_shape.bottom - ball_shape.top

				smallest = min(overlap_L, overlap_R, overlap_T, overlap_B)

				if smallest == overlap_L or smallest == overlap_R:
					ball["speed"][0] *= -1
				else:
					ball["speed"][1] *= -1

				bricks.remove(brick)
				game_state["score"] += game_state["level"]
			#end_if
		#end_for
	#end_if
#end_def

def reset_ball(ball: dict, player: pygame.Rect):
	shape: pygame.Rect = ball["shape"]

	shape.center = (
		player.centerx + ball["offset_x"],
		player.centery + ball["offset_y"]
	)
	ball["speed"] = ball["speed_original"]
#end_def

def reset_bricks(screen_size: tuple, bricks: dict):
	bricks["list"] = create_bricks(
		screen_size,
		bricks["grid"],
		bricks["spacing"],
		bricks["padding"],
		bricks["colors"],
	)["list"]
#end_def

def render_screen(state: dict, screen: dict, obj: dict):
	surface = screen["surface"]
	player = obj["player"]
	ball = obj["ball"]
	bricks = obj["bricks"]

	surface.fill(screen["bg_color"])

	pygame.draw.rect(surface, player["color"], player["shape"])
	pygame.draw.ellipse(surface, ball["color"], ball["shape"])
	for brick in bricks:
		pygame.draw.rect(surface, brick["color"], brick["shape"])
	
	font = pygame.font.Font(None, 30)
	txt_color = pygame.Color("yellow")
	score = font.render(f"Score: {state["score"]}", True, txt_color)
	lives = font.render(f"Lives: {state["lives"]}", True, txt_color)
	surface.blit(score, (0, surface.get_height() - 20))
	surface.blit(lives, (0, 0))

	pygame.display.flip()
#end_def
