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
from os.path import join as join_dirs
import random

def get_asset(dir_name: str, file_name: str) -> str:
	return join_dirs("assets", dir_name, file_name)
#end_def

def get_main_font() -> str:
	return get_asset("fonts", "Photonico-Current-Regular.ttf")
#end_def

def get_icon() -> str:
	return get_asset("images", "icon.png")
#end_def

def get_title() -> str:
	return "Brick Breaker: ASMbleia\'s edition"
#end_def

def get_background_color() -> pygame.Color:
	return pygame.Color("gray19")
#end_def

def get_secondary_color() -> pygame.Color:
	return pygame.Color("black")

def get_main_color() -> pygame.Color:
	return pygame.Color("white")
#end_def

def is_rect_inside_screen(screen_size: tuple, rect: pygame.Rect) -> bool:
	if rect.x < 0 or rect.y < 0 or rect.x + rect.width > screen_size[0] or rect.y + rect.height > screen_size[1]:
		return False
	return True
#end_def

def play_sound(file_name: str):
	pygame.mixer.Sound(get_asset("sounds", file_name)).play()
#end_def
