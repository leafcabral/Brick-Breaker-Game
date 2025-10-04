"""
ASMbleia
	Ian Caliel Matos Cabral
	João Paulo Pipper da Silva
	Rafael Cabral Lopes
	Vitor Felberg Barcelos
Serra, Brasil
Recriação simples do jogo Brick Breaker em python utilizando a biblioteca
pygame, usando como base o tutorial da Hashtag Programação, presente no link 
[https://www.youtube.com/watch?v=h0fKGPW_cxw]. Além da mudança das váriaveis
globais para escopo de função, modificando as funções, quando necessário, foram
feitos diversas mudanças para deixar o jogo e o código melhor em diversos
aspectos.
"""
import gamefuncs as gf
import pygame 

def main() -> None:
	pygame.init()
	
	# relogio para calcular delta time
	clock = pygame.time.Clock()
	screen = gf.new_screen(600, 600, "black")
	pygame.display.set_caption("Brick Breaker: ASMbleia\'s edition")
	game_state: dict = gf.new_game_state()

	player = gf.new_player(screen["surface"].get_size())
	ball = gf.new_ball(player["shape"])
	bricks = gf.create_bricks((screen["surface"].get_size()))

	game_objs: dict = {
		"player": player,
		"ball": ball,
		"bricks": bricks,
	}

	brick_respawn_delay: float = 1
	while game_state["running"]:
		game_state["delta"] = clock.tick(60) / 1_000
		key_pressed = pygame.key.get_pressed()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_state["running"] = False
			elif event.type == pygame.KEYDOWN:
				gf.handle_keydown(
					screen,
					event,
					game_state,
					game_objs
				)
		#end_for
			
		if game_state["paused"] or game_state["game_over"]:
			gf.render_screen(game_state, screen, game_objs)
			continue

		gf.move_player(
			screen,
			game_state["delta"],
			player,
			key_pressed
		)
		gf.move_ball(screen, game_state["delta"], ball)
		gf.handle_ball_collisions(game_state, ball, game_objs)

		if not gf.is_rect_inside_screen(screen, ball["shape"]):
			game_state["lives"] -= 1

			if game_state["lives"] > 0:
				gf.reset_ball(ball, player["shape"])
			else:
				game_state["game_over"] = True
		#end_if
		
		if not bricks["list"]:
			if brick_respawn_delay <= 0:
				gf.reset_bricks(
					(screen["surface"].get_size()),
					bricks
				)
				game_state["level"] += 1
				brick_respawn_delay = 1
			else:
				brick_respawn_delay -= game_state["delta"]
		#end_if

		gf.render_screen(game_state, screen, game_objs)
	#end_while

	print(f"Score: {game_state["score"]}")
	print(f"Level: {game_state["level"]}")
	pygame.quit()
#end_def

if (__name__ == "__main__"):
	main()