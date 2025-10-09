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

import graphics

def main() -> None:
	pygame.init()
	
	screen: dict = game.new_screen()
	game_state: dict = game.new_state()
	game_objs: dict = game.new_objects(screen["surface"].get_size())
	game_timers: dict = game.new_timers()

	# funcao main menu
	graphics.main_menu(screen)
	while game_state["running"]:
		# Input, timers, movimentos e mais
		game.process(screen["surface"].get_size(), game_state, game_objs, game_timers)
	
		game.render_screen(game_state, screen, game_objs)
	#end_while

	print(f"Score: {game_state['score']}")
	print(f"Level: {game_state['level']}")
	pygame.quit()
#end_def

if __name__ == "__main__":
	main()
