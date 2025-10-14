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
import pygame, utils, controls

def _render_objects(surface: pygame.Surface, objs: dict):
	player = objs["player"]
	ball = objs["ball"]
	bricks = objs["bricks"]

	pygame.draw.rect(surface, player["color"], player["shape"], border_radius=5)
	pygame.draw.ellipse(surface, ball["color"], ball["shape"])
	for brick in bricks["list"]:
		pygame.draw.rect(surface, brick["color"], brick["shape"], border_radius=5)
#end_def

def _render_texts(
		surface: pygame.Surface,
		game_state: dict,
		color: pygame.Color = pygame.Color("white")):
	font_name: str = utils.get_main_font()
	lives_font: pygame.font.Font = pygame.font.Font(font_name, 40)
	score_font: pygame.font.Font = pygame.font.Font(font_name, 25)

	lives: pygame.Surface = lives_font.render(
		"☻"*game_state["lives"] + "☺"*(3-game_state["lives"]),
		True, color
	)
	score: pygame.Surface = score_font.render(
		f"{game_state['score']:05}",
		True, color
	)

	# Centraliza a pontuação
	score_rect: pygame.Rect = score.get_rect()
	score_rect.centerx = surface.get_rect().centerx
	score_rect.y = surface.get_height() - score_rect.height - 10
	# Coloca vida na mesma posicao y da pontuacao
	lives_rect: pygame.Rect = lives.get_rect()
	lives_rect.centery = score_rect.centery

	surface.blit(lives, (12, score_rect.y - 5))
	surface.blit(score, score_rect)
#end_def

def _render_overlay(
		surface: pygame.Surface,
		title: str,
		subtitle: str = "",
		color: pygame.Color = pygame.Color("white")):
	font_name: str = utils.get_main_font()
	title_font: pygame.font.Font = pygame.font.Font(font_name, 50)
	subtitle_font: pygame.font.Font = pygame.font.Font(font_name, 20)

	title_txt: pygame.Surface = title_font.render(title, True, color)
	subtitle_txt: pygame.Surface = subtitle_font.render(
		subtitle,
		True,
		color
	)

	title_rect: pygame.Rect = title_txt.get_rect()
	subtitle_rect: pygame.Rect = subtitle_txt.get_rect()

	screen_center = surface.get_rect().center
	title_rect.center = screen_center
	subtitle_rect.center = screen_center
	subtitle_rect.centery += 30

	overlay: pygame.Surface = pygame.Surface(
		surface.get_size(),
		pygame.SRCALPHA # overlay transparente
	)
	bg_color: pygame.Color = pygame.Color("grey25")
	bg_color.a = 127
	overlay.fill(bg_color)

	surface.blit(overlay, (0,0))
	surface.blit(title_txt, title_rect)
	surface.blit(subtitle_txt, subtitle_rect)
#end_def

def main_menu(screen: dict) -> None:
	surface: pygame.Surface = screen["surface"]
	surface.fill(utils.get_background_color())

	title_size: int = 40
	subtitle_size: int = 28
	text_size: int = 24

	font: pygame.font.Font = pygame.font.Font(utils.get_main_font(), title_size)

	title_text = font.render("Brick Breaker", True, pygame.Color("white"))
	title_text_rect = title_text.get_rect()
	title_text_rect.centerx = screen["rect"].centerx
	title_text_rect.centery += title_size

	font = pygame.font.Font(utils.get_main_font(), subtitle_size)

	subtitle_text = font.render("ASMbleia\'s Edition", True, pygame.Color("white"))
	subtitle_text_rect = subtitle_text.get_rect()
	subtitle_text_rect.center = title_text_rect.center
	subtitle_text_rect.centery += title_size

	font = pygame.font.Font(utils.get_main_font(), text_size)

	text_start = font.render(f"Press {controls.action_to_str("confirm")} to start game.", True, pygame.Color("white"))
	text_start_rect = text_start.get_rect()
	text_start_rect.center = screen["rect"].center
	text_start_rect.centery -= text_size

	text_exit = font.render(f"Press {controls.action_to_str("quit")} to close game.", True, pygame.Color("white"))
	text_exit_rect = text_exit.get_rect()
	text_exit_rect.center = text_start_rect.center
	text_exit_rect.centery += text_size + 5

	surface.blit(title_text, title_text_rect)
	surface.blit(subtitle_text, subtitle_text_rect)
	surface.blit(text_start, text_start_rect)
	surface.blit(text_exit, text_exit_rect)
	
	pygame.display.flip()
	
	while True:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					quit()
				if event.key == pygame.K_RETURN: return
#end_def

def pause_menu(screen: dict) -> None:
	surface: pygame.Surface = screen["surface"]
	surface_size = surface.get_size()

	pause_menu: pygame.Surface = pygame.Surface(surface_size)
	pause_menu.fill(utils.get_secondary_color())
	pause_menu.set_alpha(192)

	font: pygame.font.Font = pygame.font.Font(utils.get_main_font(), 40)

	text = font.render("Game paused", True, pygame.Color("white"))
	text_rect = text.get_rect()
	text_rect.centerx = screen["rect"].centerx
	text_rect.centery += font.get_linesize()

	font = pygame.font.Font(utils.get_main_font(), 24)

	text_unpause = font.render(f"Press {controls.action_to_str("menu")} to unpause.", True, pygame.Color("white"))
	text_unpause_rect = text_unpause.get_rect()
	text_unpause_rect.center = screen["rect"].center
	text_unpause_rect.centery -= font.get_linesize()

	text_exit = font.render(f"Press {controls.action_to_str("quit")} to close game.", True, pygame.Color("white"))
	text_exit_rect = text_exit.get_rect()
	text_exit_rect.center = text_unpause_rect.center
	text_exit_rect.centery += font.get_linesize()

	surface.blit(pause_menu, (0, 0))
	surface.blit(text, text_rect)
	surface.blit(text_unpause, text_unpause_rect)
	surface.blit(text_exit, text_exit_rect)
#end_def

def game_over(screen: dict) ->  None:
	surface: pygame.Surface = screen["surface"]
	surfaceSize = surface.get_size()

	game_over: pygame.Surface = pygame.Surface(surfaceSize)
	game_over.fill(utils.get_secondary_color())
	game_over.set_alpha(192)

	font: pygame.font.Font = pygame.font.Font(utils.get_main_font(), 40)

	text = font.render("Game over", True, pygame.Color("red"))
	text_rect = text.get_rect()
	text_rect.centerx = screen["rect"].centerx
	text_rect.centery += font.get_linesize()

	font = pygame.font.Font(utils.get_main_font(), 24)

	text_restart = font.render(f"Press {controls.action_to_str("restart")} to restart.", True, pygame.Color("white"))
	text_restart_rect = text_restart.get_rect()
	text_restart_rect.center = screen["rect"].center
	text_restart_rect.centery -= font.get_linesize()

	text_exit = font.render(f"Press {controls.action_to_str("quit")} to close game.", True, pygame.Color("white"))
	text_exit_rect = text_exit.get_rect()
	text_exit_rect.center = text_restart_rect.center
	text_exit_rect.centery += font.get_linesize()

	surface.blit(game_over, (0, 0))
	surface.blit(text, text_rect)
	surface.blit(text_restart, text_restart_rect)
	surface.blit(text_exit, text_exit_rect)
#end_def
