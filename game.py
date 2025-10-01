"""
ASMbleia
	Ian Caliel Matos Cabral
	João Paulo Pipper da Silva
	Rafael Cabral Lopes
	Vitor Felberg Barcelos
Serra, Brasil
Recriação do jogo Brick Breakr extremamente simples em python pela biblioteca
pygame, seguindo o tutorial [https://www.youtube.com/watch?v=h0fKGPW_cxw], foi
feito a mudança das váriaveis de escopo global para escopo de função,
adicionando também parametros para as funções, quando necessário.
Além disso, também foi feita mudanças gerais no código, visando maior legibili-
dade e performance, foi mudada a checagem de tecla pressionado por event.type
para pygame.key.get_pressed(), pois o primeiro estava dando diversos problemas
TO-DO:
	- Dicionário para variaveis globais (deltaTime, screen, score)
	- Implementar tempo "delta"
	- Bola quica de forma gostosa no jogador (deixar movimento mais flúido)
	- Cada linha de tijolo tem cor diferente
	- Bola começar em cima do jogador
	- Fases (levels) com tijolos (bricks) novos (sem ser velho) com mais (+) pontos (score)
"""

from gamefuncs import *
import pygame 

def main() -> None:
	pygame.init()
	
	gameInfo: dict = {
		"screen": None,
		"delta": 0,
		"score": 0,
		"player": {
			"shape": None,
			"color": pygame.Color("white"),
			"speed": 5
		},
		"ball":  {
			"shape": None,
			"color": pygame.Color("white"),
			"speed": [5, -5]
		},
		"bricks": {
			"list": None,
			"grid": (8,5)
		}
	}

	objSizes: dict = {
		"screen": (600, 600),
		"ball": (15, 15),
		"player": (100, 15),
		"brickGrid": (8, 5)
	}

	# Criar janela
	gameInfo["screen"] = pygame.display.set_mode((600, 600))
	pygame.display.set_caption("Brick Breaker: ASMbleia\'s edition")

	ballPosition: tuple = (gameInfo["screen"].get_width() // 2, gameInfo["screen"].get_height() - 70)

	# Criar objetos
	player = pygame.Rect((gameInfo["screen"].get_width() // 2 - objSizes["player"][0] // 2, gameInfo["screen"][1] - 50), objSizes["player"])
	ball = pygame.Rect(ballPosition, objSizes["ball"])
	bricks: list = createBricks(gameInfo["screen"], objSizes["brickGrid"])

	# WARNING: ballMovement irá mudar durante o jogo, crie uma copia se preciso
	playerSpeed: float = 5
	ballMovement: list = [5, -5] # velocidade no eixo x e y

	score   = 0
	running = True
	while running:
		delta = pygame.clock.tick(60) / 1000.0 # em segundos; 60 FPS

		clearScreen(screen)
		drawObjects(screen, (player, "blue"), (ball, "white"), (bricks, "green"))
		updateScoreText(screen, score)
		
		movePlayer(gameInfo["screen"], pygame.key.get_pressed(), player, playerSpeed)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		#end_for

		score, ballMovement = moveBall(gameInfo["screen"], ball, ballMovement, player, bricks, score)
		# Se bola encostou no "chao" ou não tem mais tijolo (game over / vitoria)
		if (not ballMovement) or (not bricks):
			running = False
		
		pygame.time.wait()
		updateScreen()
	#end_while

	# Se pontuacao maxima tiver sido alcancada
	if not bricks:
		print("\nYOU WIN!")
	else:
		print("\nGAME OVER :(")

	pygame.quit()
#end_def

if (__name__ == "__main__"):
	main()