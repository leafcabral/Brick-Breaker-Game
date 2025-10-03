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
	- [X] Dicionário para variaveis globais (deltaTime, screen, score)
	- [ ] Implementar tempo "delta"
	- [ ] Rebate da bola depende de onde acertar no jogador
	- [ ] Colisão com tijolo realista
	- [X] Cada linha de tijolo tem cor diferente
	- [X] Bola começar em cima do jogador
	- [ ] Fases com tijolos valendo mais pontos
	- [ ] Sistema de vidas
"""
import gamefuncs
import pygame 

def main() -> None:
	pygame.init()
	
	# relogio para calcular delta time
	clock = pygame.time.Clock()
	screen = gamefuncs.newScreen(600, 600, "black")
	pygame.display.set_caption("Brick Breaker: ASMbleia\'s edition")
	game_state: dict = {
		"delta": 0,
		"lives": 3,
		"score": 0,
		"level": 1,
		"running": True,
		"paused": False,
	}

	player = gamefuncs.newPlayer(
		(screen["width"] // 2, screen["height"] - 50)
	)
	player_center: tuple = player["shape"].center
	ball = gamefuncs.newBall(
		(player_center[0], player_center[1] + 10)
	)
	bricks = gamefuncs.createBricks(
		screen_size=(screen["width"], screen["height"]),
		grid=(5,4),
		level=game_state["level"],
	)

	game_obj: dict = {
		"player": player,
		"balls": [ball],
		"bricks": bricks,
	}

	while game_state["running"]:
		game_state["delta"] = clock.tick(60) / 1_000
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_state["running"] = False
		#end_for

		gamefuncs.movePlayer(
			screen,
			game_state,
			player,
			pygame.key.get_pressed()
		)
		
		game_state["score"], ball["speed"] = gamefuncs.moveBall(game_state["screen"], ball, ball["speed"], player, bricks, game_state["score"])
		# Se bola encostou no "chao" ou não tem mais tijolo (game over / vitoria)
		if (not ball["speed"]) or (not bricks):
			game_state["running"] = False
		
		gamefuncs.renderScreen(game_state, screen, game_obj)
	#end_while

	print(f"Score: {game_state["score"]}")
	pygame.quit()
#end_def

if (__name__ == "__main__"):
	main()