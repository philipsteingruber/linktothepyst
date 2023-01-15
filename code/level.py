import pygame
from settings import WORLD_MAP, TILESIZE
from tile import Tile
from player import Player
from debug import debug

class Level():
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.setup_grid()

    def setup_grid(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, cell in enumerate(row):
                if cell:
                    x_pos = col_index * TILESIZE
                    y_pos = row_index * TILESIZE
                    if cell == 'x':
                        Tile((x_pos, y_pos), [self.visible_sprites, self.obstacle_sprites])
                    if cell == 'p':
                        Player((x_pos, y_pos), self.visible_sprites)



    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.obstacle_sprites.draw(self.display_surface)
        debug(len(self.visible_sprites), len(self.obstacle_sprites))