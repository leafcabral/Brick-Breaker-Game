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
import controls

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
		"ball_thrown": False 
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
	state["ball_thrown"] = False

	if state["lives"] > 0:
		entities.reset_ball(objs["ball"], objs["player"])
	else:
		state["game_over"] = True
#end_def

def respawn_bricks(timers: dict, objs: dict):
	timer_name: str = "brick_respawn"
	
	if timer_name not in timers:
		timers[timer_name] = 0
	elif timers[timer_name] <= 0:
		del timers[timer_name]
		
		entities.create_brick_list(objs["bricks"])
	#end_if
#end_def

def reset_game(state: dict, objs: dict):
	state.update(new_state())
	
	entities.reset_player(objs["player"])
	entities.reset_ball(objs["ball"], objs["player"])
	entities.create_brick_list(objs["bricks"])
#end_def

def handle_keydown(events: list, state: dict, objs: dict):
	if controls.was_pressed("menu", events):
		state["paused"] = not state["paused"]

	if controls.was_pressed("quit", events) and \
			(state["paused"] or state["game_over"]):
		state["running"] = False
	if controls.was_pressed("restart", events) and state["game_over"]:
		#print_stats(state)
		reset_game(state, objs)
#end_def

def process(screen_size: tuple, game_state: dict, game_objs: dict, game_timers: dict) -> None:
	update_timers(game_timers)

	# Move os tijolos para baixo
	if game_objs["bricks"]["pos_start"][1] < 50 and not (game_state["paused"] or game_state["game_over"]):
		game_objs["bricks"]["pos_start"][1] += 1
		respawn_bricks(game_timers, game_objs)

	events: list = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			game_state["running"] = False
	#end_for
	
	handle_keydown(events, game_state, game_objs)
	
	if game_state["paused"] or game_state["game_over"]:
		return

	# Move todas as entidades
	movement.move_player(
		screen_size,
		game_timers["delta"],
		game_objs["player"]
	)

	if game_state["ball_thrown"]:
		movement.move_ball(screen_size, game_timers["delta"], game_objs["ball"])
		movement.handle_ball_collisions(game_state, game_objs)
	elif not start_game(game_objs, events, game_state):
		return

	if is_out_of_bounds(game_objs["ball"], screen_size):
		consume_live(game_state, game_objs)

	# Se acabar os tijolos
	if not game_objs["bricks"]["list"]:
		game_objs["bricks"]["pos_start"][1] = -200
		respawn_bricks(game_timers, game_objs)
		game_state["level"] += 1
	#end_if
#end_def

def is_out_of_bounds(ball:dict, screen_size: tuple) -> bool:
	return ball["shape"].centery + ball["radius"] >= screen_size[1]
#end_def

def render_screen(game_state: dict, screen: dict, game_objs: dict):
	surface: pygame.Surface = screen["surface"]

	surface.fill(screen["bg_color"])

	graphics._render_objects(surface, game_objs)
	graphics._render_texts(surface, game_state)

	if game_state["paused"]:
		graphics.pause_menu(screen)
	if game_state["game_over"]:
		graphics.game_over(screen)

	pygame.display.flip()
#end_def

def start_game(game_objs: dict, events: list, game_state: dict) -> bool:
	player_rect: pygame.Rect = game_objs["player"]["shape"]
	ball: dict = game_objs["ball"]
	circle: pygame.Rect = ball["shape"]

	circle.centery = player_rect.centery - (player_rect.height/2) - 10 - ball["radius"]
	circle.centerx = player_rect.centerx

	for event in events:
		if event.type == pygame.QUIT:
			game_state["running"] = False

	if controls.is_pressed("up") or controls.is_pressed("throw"):
		game_state["ball_thrown"] = True
		return True
	
	return False
