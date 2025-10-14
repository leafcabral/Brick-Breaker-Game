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

def actions_dict() -> dict:
	return {
		"left": [pygame.K_LEFT, pygame.K_a],
		"right": [pygame.K_RIGHT, pygame.K_d],
		"up": [pygame.K_UP, pygame.K_w],
		"down": [pygame.K_DOWN, pygame.K_s],
		"throw": [pygame.K_SPACE],

		"confirm": [pygame.K_RETURN],
		"menu": [pygame.K_ESCAPE, pygame.K_p],
		"quit": [pygame.K_q],
		"restart": [pygame.K_r]
	}
#end_def

def is_pressed(action: str) -> bool:
	keys_pressed: tuple = pygame.key.get_pressed()
	actions: dict = actions_dict()

	if action not in actions:
		return False

	for key in actions[action]:
		if keys_pressed[key]:
			return True
	
	return False
#end_def

def was_pressed(action: str, events: list) -> bool:
	actions: dict = actions_dict()

	if action not in actions:
		return False
		
	for event in events:
		if event.type != pygame.KEYDOWN:
			continue

		for key in actions[action]:
			if event.key == key:
				return True
	
	return False
#end_def

def get_action_keys(action: str) -> list:
	actions: dict = actions_dict()

	if action not in actions:
		return None
	else:
		return actions[action]
#end_def

def get_action_keys_strings(action: str) -> list:
	keys: list = get_action_keys(action)

	if keys == None:
		return None
	
	strings: list = []
	for key in keys:
		strings.append(pygame.key.name(key).upper())
	
	return strings
#end_def