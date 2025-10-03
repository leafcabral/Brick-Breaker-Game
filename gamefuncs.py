"""
ASMbleia
	Ian Caliel Matos Cabral
	João Paulo Pipper da Silva
	Rafael Cabral Lopes
	Vitor Felberg Barcelos
Serra, Brasil
Recriação do jogo Brick Breakr extremamente simples em python pela biblioteca
pygame, seguindo o tutorial [https://www.youtube.com/watch?v=h0fKGPW_cxw], foi
feito a mudança das váriaveis de escopo global para escopo de função, adicio-
nando também parametros para as funções, quando necessário.
Além disso, também foi feita mudanças gerais no código, visando maior legibili-
dade e performance, foi mudada a checagem de tecla pressionado por event.type
para pygame.key.get_pressed(), pois o primeiro estava dando diversos problemas
"""
import pygame

def newScreen(
		width: int = 600,
		height: int = 600,
		bg_color: str = "black") -> dict:
	surface = pygame.display.set_mode((width, height))
	screen: dict = {
		"surface": surface,
		"width": width,
		"height": height,
		"bg_color": pygame.Color(bg_color),
	}

	return screen
#end_def

def newPlayer(
		position: tuple,
		size: tuple = (100, 5),
		color: str = "white",
		speed: float = 5) -> dict:
	return {
		"shape": pygame.Rect(position, size),
		"position": position,
		"size": size,
		"color": pygame.Color(color),
		"speed": speed,
	}
#end_def

def newBall(
		center: tuple,
		radius: float = 10,
		color: str = "white",
		speed: list = [5, -5]) -> dict:
	topLeftCorner: tuple = (center[0] - radius, center[1] - radius)
	diameter: float = radius*2

	ball: dict = {
		"shape": pygame.Rect(topLeftCorner, (diameter, diameter)),
		"position": topLeftCorner,
		"center": center,
		"radius": radius,
		"size": (radius, radius),
		"color": pygame.Color(color),
		"speed": speed,
	}

	return ball
#end_def

def newBrick(position: list, size: tuple, color: str, score: int) -> dict:
	return {
		"shape": pygame.Rect(position, size),
		"color": pygame.Color(color),
		"score": score,
	}
#end_def

def createBricks(
		screen_size: tuple,
		grid: tuple = (5,4),
		spacing: int = 5,
		level: int = 1,
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
			bricks.append(newBrick(pos, size, color, level))

			pos[0] += increment[0]
		#end_for
			
		pos[1] += increment[1]
	#end_for

	return bricks
#end_def

def movePlayer(screenSize: tuple, keys, player, speed: float):
	if keys[pygame.K_RIGHT] and (player.x + player.width) < screenSize[0]:
		player.x += speed
	if keys[pygame.K_LEFT] and player.x > 0:
		player.x -= speed
	#end_match
#end_def

def moveBall(screenSize: tuple, ball, ballMovement: list, player, bricks: list, score: int) -> tuple:
	ball.x += ballMovement[0]
	ball.y += ballMovement[1]

	# Checa por colisao com as paredes e o teto
	if (ball.x <= 0) or ((ball.x + ball.width) >= screenSize[0]):
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
	if ((ball.y + ball.height) >= screenSize[1]):
		ballMovement = []

	return (score, ballMovement)
#end_def


def renderScreen(state: dict, screen: dict, obj: dict):
	surface = screen["surface"]
	player = obj["player"]
	balls = obj["ball"]
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
	score = font.render(f"Score: {state["score"]}", True, txt_color)
	lives = font.render(f"Lives: {state["lives"]}", True, txt_color)
	surface.blit(score, (0, screen["height"] - 20))
	surface.blit(lives, (0, 0))

	pygame.display.flip()
#end_def
