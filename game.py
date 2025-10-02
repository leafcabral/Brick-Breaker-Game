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
	- Rebate da bola depende de onde acertar no jogador
	- Colisão com tijolo realista
	- Cada linha de tijolo tem cor diferente
	- Bola começar em cima do jogador
	- Fases com tijolos valendo mais pontos
	- Sistema de vidas
"""
import gamefuncs
import pygame 

def main() -> None:
	pygame.init()
	
	screen = gamefuncs.newScreen(600, 600, "black")
	pygame.display.set_caption("Brick Breaker: ASMbleia\'s edition")
	game_state: dict = {
		"deltaTime": 0,
		"score": 0,
		"level": 1,
		"running": True,
		"paused": False,
	}

	player = gamefuncs.newPlayer(
		position=(screen["width"]//2, screen["height"]-50),
		size=(100, 5),
		color="white",
		speed=5,
	)
	player_center: tuple = player["shape"].center
	ball = gamefuncs.newBall(
		center=(player_center[0], player_center[1]+10),
		radius=10,
		color="white",
		speed=[5, -5],
	)
	bricks = gamefuncs.createBricks(
		screen_size=(screen["width"], screen["height"]),
		grid=(5,4),
		spacing=5,
		level=game_state["level"],
		colors=["blue", "red", "yellow", "green"],
	)

	while game_state["running"]:
		#delta = pygame.clock.tick(60) / 1000.0 # em segundos; 60 FPS

		gamefuncs.clearScreen(screen)
		gamefuncs.drawObjects(screen, (player, "blue"), (ball, "white"), (bricks, "green"))
		gamefuncs.updateScoreText(screen, game_state["score"])
		
		gamefuncs.movePlayer(game_state["screen"], pygame.key.get_pressed(), player, player["speed"] playerSpeed)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		#end_for

		game_state["score"], ballMovement =gamefuncs. moveBall(game_state["screen"], ball, ball["speed"], player, bricks, game_state["score"])
		# Se bola encostou no "chao" ou não tem mais tijolo (game over / vitoria)
		if (not ballMovement) or (not bricks):
			running = False
		
		pygame.time.wait(10)
		gamefuncs.updateScreen()
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