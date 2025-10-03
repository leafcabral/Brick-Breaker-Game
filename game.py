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
"""
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
	screen = gamefuncs.new_screen(600, 600, "black")
	pygame.display.set_caption("Brick Breaker: ASMbleia\'s edition")
	game_state: dict = {
		"delta": 0,
		"lives": 3,
		"score": 0,
		"level": 1,
		"running": True,
		"paused": False,
	}

	player = gamefuncs.new_player(
		(screen["surface"].width // 2, screen["surface"].height - 50)
	)
	ball = gamefuncs.new_ball(
		(player["shape"].centerx, player["shape"].centery - 10)
	)
	bricks = gamefuncs.create_bricks(
		screen_size=(screen["surface"].get_size()),
		grid=(5,4),
	)

	game_obj: dict = {
		"player": player,
		"balls": [ball],
		"bricks": bricks,
	}

	while game_state["running"]:
		game_state["delta"] = clock.tick(60) / 1_000
		key_pressed = pygame.key.get_pressed()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_state["running"] = False
			elif key_pressed[pygame.K_p] \
					or key_pressed[pygame.K_ESCAPE]:
				game_state["paused"] = not game_state["paused"]
		#end_for

		if not game_state["paused"]:
			gamefuncs.move_player(
				screen["surface"].get_size(),
				game_state["delta"],
				player,
				key_pressed
			)

			gamefuncs.move_ball(
				screen["surface"].get_size(),
				game_state,
				ball,
				game_obj
			)

			if game_state["lives"] <= 0:
				game_state["running"] = False
		#end_if
		
		gamefuncs.render_screen(game_state, screen, game_obj)
	#end_while

	print(f"Score: {game_state["score"]}")
	pygame.quit()
#end_def

if (__name__ == "__main__"):
	main()