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
from turtle import color
import pygame

def newScreen(width: int, height: int, bgColor: str) -> dict:
	surface = pygame.display.set_mode((width, height))
	screen: dict = {
		"surface": surface,
		"width": width,
		"height": height,
		"bg_color": pygame.Color(bgColor),
	}

	return screen
#end_def

def newPlayer(position: tuple, size: tuple, color: str, speed: float) -> dict:
	return {
		"shape": pygame.Rect(position, size),
		"position": position,
		"size": size,
		"color": pygame.Color(color),
		"speed": speed,
	}
#end_def

def newBall(center: tuple, radius: float, color: str, speed: list) -> dict:
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
		grid: tuple,
		spacing: int,
		level: int,
		colors: list) -> list:
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

def clearScreen(screen):
	screen.fill(pygame.Color("black"))
#end_def

def updateScreen():
	pygame.display.flip()
#end_def

def drawObjects(screen, player: tuple, ball: tuple, bricks: tuple):
	pygame.draw.rect(screen, pygame.Color(player[1]), player[0])
	pygame.draw.ellipse(screen, pygame.Color(ball[1]), ball[0])
	for brick in bricks[0]:
		pygame.draw.rect(screen, pygame.Color(bricks[1]), brick)
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

def updateScoreText(screen, score):
	font = pygame.font.Font(None, 30)
	text = font.render(f"Iscóri: {score}", True, pygame.Color("cyan"))
	screen.blit(text, (0, screen.get_height() - 20))
#end_def