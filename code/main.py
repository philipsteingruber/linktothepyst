import os
import sys

import pygame

from level import Level
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, WATER_COLOR


class Game:
	def __init__(self):
		# General setup
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('Zelda - A Link to the PYst')
		self.clock = pygame.time.Clock()

		self.level = Level()

		music = pygame.mixer.Sound('../audio/main.ogg')
		music.set_volume(0.1)
		music.play(loops=-1)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						self.level.toggle_upgrade_menu()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()

			self.clock.tick(FPS)


if __name__ == '__main__':
	lines = 0
	for filename in os.listdir('./'):
		try:
			with open(filename) as file:
				linecount = len(file.readlines())
				print(filename, linecount)
				lines += linecount
		except PermissionError:
			pass
	print('Full Linecount:', lines)

	game = Game()
	game.run()
