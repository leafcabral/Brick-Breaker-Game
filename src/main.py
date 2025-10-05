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
import pygame 
import game
import gamefuncs as gf

def main() -> None:
	pygame.init()
	
	screen: dict = game.new_screen()
	game_state: dict = game.new_state()
	game_objs: dict = game.new_objects(screen["surface"].get_size())
	timers: dict = game.new_timers()

	game.new_timer(timers, "brick_respawn", 2)

	while game_state["running"]:
		game.get_delta(timers)
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
			timers["delta"],
			game_objs["player"],
			key_pressed
		)
		gf.move_ball(screen, timers["delta"], game_objs["ball"])
		gf.handle_ball_collisions(
			game_state,
			game_objs["ball"],
			game_objs
		)

		if not gf.is_rect_inside_screen(
				screen, 
				game_objs["ball"]["shape"]
			):
			game_state["lives"] -= 1

			if game_state["lives"] > 0:
				game.reset_ball(game_objs)
			else:
				game_state["game_over"] = True
		#end_if
		
		if not game_objs["bricks"]["list"]:
			if timers["brick_respawn"] <= 0:
				game.reset_bricks(
					(screen["surface"].get_size()),
					game_objs
				)
				game_state["level"] += 1
				timers["brick_respawn"] = timers[
					"brick_respawn_original"
				]
			else:
				timers["brick_respawn"] -= timers["delta"]
		#end_if

		gf.render_screen(game_state, screen, game_objs)
	#end_while

	print(f"Score: {game_state["score"]}")
	print(f"Level: {game_state["level"]}")
	pygame.quit()
#end_def

if __name__ == "__main__":
	main()