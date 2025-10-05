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

def new_objects(screen_size: tuple) -> dict:
	player: dict = entities.new_player(screen_size)
	ball: dict = entities.new_ball(player)
	bricks: dict = entities.create_bricks(screen_size)

	return {
		"player": player,
		"ball": ball,
		"bricks": bricks,
	}
#end _def

def new_timers():
	clock = pygame.time.Clock()

	return {
		"clock": clock,
		"delta": 0,
		# adiciona outros timers durante o jogo aqui
	}
#end _def

def get_delta(timer: dict) -> float:
	timer["delta"] = timer["clock"].tick(60) / 1_000

	return timer["delta"]
#end_def

def new_timer(timer: dict, name: str, time: float):
	timer[name] = time
	timer[name + "_original"] = time
#end_def

def reset_game_state(game_state: dict):
	temp: dict = new_state()
	game_state.clear()
	game_state.update(temp)
#end_def

def reset_ball(objs: dict):
	objs["ball"] = entities.new_ball(
		objs["player"],
		objs["ball"]["radius"]
	)
#end_def

def reset_bricks(screen_size: tuple, objs: dict):
	old: dict = objs["bricks"]
	objs["dict"] = entities.create_bricks(screen_size, old["grid"])
#end_def

def reset_game(screen_size: tuple, state: dict, objs: dict):
	pass
#end_def