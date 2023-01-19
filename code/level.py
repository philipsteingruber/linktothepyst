import pygame
from settings import WORLD_MAP, TILESIZE
from tile import Tile
from player import Player
from debug import debug

class Level():
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = None
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
                        self.player = Player(pos=(x_pos, y_pos), groups=self.visible_sprites, obstacle_sprites=self.obstacle_sprites)



    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)

        # self.obstacle_sprites.draw(self.display_surface)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(0, 0)

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        