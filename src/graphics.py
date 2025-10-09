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
import pygame, utils

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

	titleSize: int = 40
	subtitleSize: int = 28
	textSize: int = 24

	font: pygame.font.Font = pygame.font.Font(utils.get_main_font(), titleSize)

	titleText = font.render("Brick Breaker", True, pygame.Color("white"))
	titleTextRect = titleText.get_rect()
	titleTextRect.centerx = screen["rect"].centerx
	titleTextRect.centery += titleSize

	font = pygame.font.Font(utils.get_main_font(), subtitleSize)

	subtitleText = font.render("ASMbleia\'s Edition", True, pygame.Color("white"))
	subtitleTextRect = subtitleText.get_rect()
	subtitleTextRect.center = titleTextRect.center
	subtitleTextRect.centery += titleSize

	font = pygame.font.Font(utils.get_main_font(), textSize)

	textStart = font.render("Press Enter to start game.", True, pygame.Color("white"))
	textStartRect = textStart.get_rect()
	textStartRect.center = screen["rect"].center
	textStartRect.centery -= textSize

	textExit = font.render("Press Q to close game.", True, pygame.Color("white"))
	textExitRect = textExit.get_rect()
	textExitRect.center = textStartRect.center
	textExitRect.centery += textSize + 5

	surface.blit(titleText, titleTextRect)
	surface.blit(subtitleText, subtitleTextRect)
	surface.blit(textStart, textStartRect)
	surface.blit(textExit, textExitRect)
	
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
	surfaceSize = surface.get_size()

	pauseMenu: pygame.Surface = pygame.Surface(surfaceSize)
	pauseMenu.fill(utils.get_secondary_color())
	pauseMenu.set_alpha(192)

	font: pygame.font.Font = pygame.font.Font(utils.get_main_font(), 40)

	text = font.render("Game paused", True, pygame.Color("white"))
	textRect = text.get_rect()
	textRect.centerx = screen["rect"].centerx
	textRect.centery += font.get_linesize()

	font = pygame.font.Font(utils.get_main_font(), 24)

	textUnpause = font.render("Press ESC to unpause.", True, pygame.Color("white"))
	textUnpauseRect = textUnpause.get_rect()
	textUnpauseRect.center = screen["rect"].center
	textUnpauseRect.centery -= font.get_linesize()

	textExit = font.render("Press Q to close game.", True, pygame.Color("white"))
	textExitRect = textExit.get_rect()
	textExitRect.center = textUnpauseRect.center
	textExitRect.centery += font.get_linesize()

	surface.blit(pauseMenu, (0, 0))
	surface.blit(text, textRect)
	surface.blit(textUnpause, textUnpauseRect)
	surface.blit(textExit, textExitRect)

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
