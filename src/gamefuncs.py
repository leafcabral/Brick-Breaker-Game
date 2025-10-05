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
import game

def handle_keydown(
		screen: dict,
		event: pygame.event.Event,
		state: dict,
		objs: dict):
	match event.key:
		case pygame.K_ESCAPE | pygame.K_p:
			state["paused"] = not state["paused"]
		case pygame.K_r:
			if state["game_over"]:
				print(f"Score: {state["score"]}")
				print(f"Level: {state["level"]}")

				game.reset_game_state(state)
				game.reset_ball(objs)
				game.reset_bricks(
					screen["surface"].get_size(),
					objs
				)
				
		case pygame.K_q:
			if state["game_over"] or state["paused"]:
				state["running"] = False
#end_def

def is_rect_inside_screen(screen: dict, rect: pygame.Rect) -> bool:
	return screen["rect"].contains(rect)
#end_def

def clamp_rect_to_screen(screen: dict, rect: pygame.Rect):
	rect.clamp_ip(screen["rect"])
#end_def

def move_player(screen: dict, delta: float, player: dict, keys):
	shape: pygame.Rect = player["shape"]
	pos_increment: int = int(player["speed"] * delta)
	
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		shape.x += pos_increment
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		shape.x -= pos_increment

	if not is_rect_inside_screen(screen, shape):
		clamp_rect_to_screen(screen, shape)
#end_def

def move_ball(screen: dict, delta: float, ball: dict):
	shape: pygame.Rect = ball["shape"]
	screen_rect: pygame.Rect = screen["rect"]

	shape.x += ball["speed"][0] * delta
	shape.y += ball["speed"][1] * delta

	if not is_rect_inside_screen(screen, shape):
		if shape.left < screen_rect.left \
				or shape.right > screen_rect.right:
			ball["speed"][0] *= -1
			clamp_rect_to_screen(screen, shape)
		elif shape.top < screen_rect.top:
			ball["speed"][1] *= -1
			clamp_rect_to_screen(screen, shape)
	#end_if
#end_def

def handle_ball_collisions(game_state: dict, ball: dict, game_objs: dict):
	ball_shape: pygame.Rect = ball["shape"]
	player_shape: pygame.Rect = game_objs["player"]["shape"]
	bricks: list = game_objs["bricks"]["list"]

	if ball_shape.colliderect(player_shape):
		# posição relativa do bola do centro do jogador
		# escala de -1 a 1 quanto a essa distancia
		hit_position: float = ball_shape.centerx - player_shape.centerx
		scale: float = hit_position / (float(player_shape.width) / 2)

		ball["speed"][0] = ball["speed_original"][0] * scale * 2
		ball["speed"][1] *= -1
		
		#ball_shape.bottom = player_shape.bottom
	else:
		for brick in bricks.copy():
			brick_shape: pygame.Rect = brick["shape"]

			if ball_shape.colliderect(brick_shape):
				# Quanto maior a velocidade
				# Maior a chance de error
				overlap_L: int = ball_shape.right - brick_shape.left
				overlap_R: int = brick_shape.right - ball_shape.left
				overlap_T: int = ball_shape.bottom - brick_shape.top
				overlap_B: int = brick_shape.bottom - ball_shape.top

				smallest = min(overlap_L, overlap_R, overlap_T, overlap_B)

				if smallest == overlap_L or smallest == overlap_R:
					ball["speed"][0] *= -1
				else:
					ball["speed"][1] *= -1

				bricks.remove(brick)
				game_state["score"] += game_state["level"]
			#end_if
		#end_for
	#end_if
#end_def

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
		f"{game_state["score"]:05}",
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

def _render_overley(
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

def render_screen(game_state: dict, screen: dict, objs: dict):
	surface: pygame.Surface = screen["surface"]

	surface.fill(screen["bg_color"])

	_render_objects(surface, objs)
	_render_texts(surface, game_state)

	leave: str = "Press Q to leave or "
	if game_state["paused"]:
		_render_overley(
			surface,
			"Game Paused",
			leave + "Press P to unpause"
		)
	if game_state["game_over"]:
		_render_overley(
			surface,
			"Game Over",
			leave + "R to restart"
		)

	pygame.display.flip()
#end_def
