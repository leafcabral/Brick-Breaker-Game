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
import utils
import entities
import movement
import graphics

def new_screen(width: int = 600, height: int = 600) -> dict:
	title: str = utils.get_title()
	icon: pygame.Surface = pygame.image.load(utils.get_icon())
	bg_color: pygame.Color = utils.get_background_color()

	surface: pygame.Surface = pygame.display.set_mode((width, height))
	screen: dict = {
		"surface": surface,
		"rect": surface.get_rect(),
		"bg_color": bg_color,
	}

	pygame.display.set_caption(title)
	pygame.display.set_icon(icon)
	
	surface.fill(bg_color)

	return screen
#end _def

def new_state(lives: int = 3) -> dict:
	return {
		"lives": lives,
		"score": 0,
		"level": 1,
		"running": True,
		"game_over": False,
		"paused": False,
	}
#end _def

def new_objects(
		screen_size: tuple,
		ball_radius: int = 10,
		brick_grid: tuple = (7,4)) -> dict:
	player: dict = entities.new_player(screen_size)
	ball: dict = entities.new_ball(player, ball_radius)
	bricks: dict = entities.create_bricks(screen_size, brick_grid)

	return {
		"player": player,
		"ball": ball,
		"bricks": bricks,
	}
#end _def

def new_timers():
	clock = pygame.time.Clock()

	return {
		"_clock": clock,
		"delta": 0,
		# adiciona outros timers durante o jogo aqui
	}
#end _def

def update_timers(game_timer: dict):
	game_timer["delta"] = game_timer["_clock"].tick(60) / 1_000

	for i in game_timer.keys():
		if not (i == "delta" or i == "_clock"):
			game_timer[i] -= game_timer["delta"]
#end_def


def consume_live(state: dict, objs: dict):
	state["lives"] -= 1

	if state["lives"] > 0:
		entities.reset_ball(objs["ball"], objs["player"])
	else:
		state["game_over"] = True
#end_def

def respawn_bricks(state: dict, timers: dict, objs: dict):
	timer_name: str = "brick_respawn"
	
	if timer_name not in timers:
		timers[timer_name] = 2
	elif timers[timer_name] <= 0:
		del timers[timer_name]
		
		entities.create_brick_list(objs["bricks"])
		state["level"] += 1
	#end_if
#end_def

def reset_game(state: dict, objs: dict):
	state.update(new_state())
	
	entities.reset_player(objs["player"])
	entities.reset_ball(objs["ball"], objs["player"])
	entities.create_brick_list(objs["bricks"])
#end_def

def handle_keydown(event: pygame.event.Event, state: dict, objs: dict):
	match event.key:
		case pygame.K_ESCAPE | pygame.K_p:
			if not state["game_over"]:
				state["paused"] = not state["paused"]
		case pygame.K_r:
			if state["game_over"]:
				print(f"Score: {state["score"]}")
				print(f"Level: {state["level"]}")

				reset_game(state, objs)
		case pygame.K_q:
			if state["game_over"] or state["paused"]:
				state["running"] = False
#end_def

def process(screen_size: tuple, game_state: dict, game_objs: dict, game_timers: dict) -> None:
	update_timers(game_timers)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_state["running"] = False
		elif event.type == pygame.KEYDOWN:
			handle_keydown(event, game_state, game_objs)
	#end_for
	
	if game_state["paused"] or game_state["game_over"]:
		return

	# Move todas as entidades
	keys_pressed: tuple = pygame.key.get_pressed()
	movement.move_player(
		screen_size,
		game_timers["delta"],
		game_objs["player"],
		keys_pressed
	)
	movement.move_ball(screen_size, game_timers["delta"], game_objs["ball"])
	movement.handle_ball_collisions(
		game_state,
		game_objs["ball"],
		game_objs
	)

	# Se bola fora da tela
	if not utils.is_rect_inside_screen(
			screen_size,
			game_objs["ball"]["shape"]):
		consume_live(game_state, game_objs)
	
	# Se acabar os tijolos
	if not game_objs["bricks"]["list"]:
		respawn_bricks(game_state, game_timers, game_objs)
	#end_if
#end_def

def render_screen(game_state: dict, screen: dict, game_objs: dict):
	surface: pygame.Surface = screen["surface"]

	surface.fill(screen["bg_color"])

	graphics._render_objects(surface, game_objs)
	graphics._render_texts(surface, game_state)

	leave: str = "Press ESC to leave or "
	if game_state["paused"]:
		graphics.pauseMenu(screen)
		# graphics._render_overlay(
		# 	surface,
		# 	"Game Paused",
		# 	leave + "Press P to unpause"
		# )
	if game_state["game_over"]:
		graphics._render_overlay(
			surface,
			"Game Over",
			leave + "R to restart"
		)

	pygame.display.flip()
#end_def