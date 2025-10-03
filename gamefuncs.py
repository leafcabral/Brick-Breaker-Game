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
		center: tuple,
		radius: float = 10,
		color: str = "white",
		speed: list = [5, -5]) -> dict:
	topLeftCorner: tuple = (center[0] - radius, center[1] - radius)
	diameter: float = radius*2

	ball: dict = {
		"shape": pygame.Rect(topLeftCorner, (diameter, diameter)),
		"radius": radius,
		"color": pygame.Color(color),
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

def is_rect_inside_screen(screen_size: tuple, rect: pygame.Rect) -> bool:
	left_right: bool = rect.x > 0 \
		and rect.x + rect.width < screen_size[0]
	top_bottom: bool = rect.y > 0 \
		and rect.y + rect.height < screen_size[1]
	
	return left_right and top_bottom
#end_def

def move_player(screen_size: tuple, delta: float, player: dict, keys):
	shape: pygame.Rect = player["shape"]
	pos_increment: int = int(player["speed"] * delta)
	
	if (is_rect_inside_screen(screen_size, shape)):
		if keys[pygame.K_RIGHT]:
			shape.x += pos_increment
		if keys[pygame.K_LEFT]:
			shape.x -= pos_increment
#end_def

def move_ball(
		screen_size: tuple,
		game_state: dict,
		ball: dict,
		game_obj: dict):
	
	...
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
	balls = obj["balls"]
	bricks = obj["bricks"]

	surface.fill(screen["bg_color"])

	pygame.draw.rect(surface, player["color"], player["shape"])
	for ball in balls:
		pygame.draw.circle(
			surface,
			ball["color"],
			ball["center"],
			ball["radius"]
		)
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
