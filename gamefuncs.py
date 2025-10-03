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
		size: tuple = (100, 5),
		color: str = "white",
		speed: float = 5) -> dict:
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
		speed: list = [5, -5],
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
		"speed_original": speed,
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
		grid: tuple = (5,4),
		spacing: int = 5,
		colors: list = ["blue", "red", "yellow", "green"]) -> list:
	qtd_cores: int = len(colors)
	bricks: list = []

	# Blocos vao até 1/4 da tela
	size: tuple = (
		(screen_size[0] - spacing) // grid[0] - spacing,
		((screen_size[1] // 4) - spacing) // grid[1] - spacing,
	)

	increment: tuple = (
		spacing + size[0],
		spacing + size[1],
	)
	
	pos: list = [spacing, spacing]
	for line in range(grid[1]):
		# Usa-se modulo para repetir a lista caso grid > lista
		color = colors[line % grid[1]]

		for column in range(grid[0]):
			bricks.append(new_brick(pos, size, color))

			pos[0] += increment[0]
		#end_for
			
		pos[1] += increment[1]
	#end_for

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
	
	if keys[pygame.K_RIGHT]:
		shape.x += pos_increment
	if keys[pygame.K_LEFT]:
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

	...
#end_def

def reset_ball(ball: dict, player: pygame.Rect):
	shape: pygame.Rect = ball["shape"]

	shape.center = (
		player.centerx + ball["offset_x"],
		player.centery + ball["offset_y"]
	)
	ball["speed"] = ball["speed_original"]
#end_def

def move_ball_deprecated(
		screen_size: tuple,
		ball,
		ballMovement: list,
		player,
		bricks: list,
		score: int) -> tuple:
	ball.x += ballMovement[0]
	ball.y += ballMovement[1]

	# Checa por colisao com as paredes e o teto
	if (ball.x <= 0) or ((ball.x + ball.width) >= screen_size[0]):
		ballMovement[0] *= -1
	if (ball.y <= 0):
		ballMovement[1] *= -1

	# Checa por colisao com objetos
	if player.colliderect(ball):
		ballMovement[1] *= -1
	for brick in bricks:
		if brick.colliderect(ball):
			bricks.remove(brick)
			ballMovement[1] *= -1
			score += 1
		#end_if
	#end_for
		
	# Checa se bola encostou no "chao"
	if ((ball.y + ball.height) >= screen_size[1]):
		ballMovement = []

	return (score, ballMovement)
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
	txt_color = pygame.Color("white")
	score = font.render(f"Score: {state['score']}", True, txt_color)
	lives = font.render(f"Lives: {state['lives']}", True, txt_color)
	surface.blit(score, (0, screen["height"] - 20))
	surface.blit(lives, (0, 0))

	pygame.display.flip()
#end_def
