import sys

import pygame
from level import Level
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH


class Game:
	def __init__(self):
		# General setup
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('Zelda - A Link to the PYst')
		self.clock = pygame.time.Clock()

		self.level = Level()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()

			self.clock.tick(FPS)


if __name__ == '__main__':
	game = Game()
	game.run()
