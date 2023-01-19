import pygame
from settings import WORLD_MAP, TILESIZE
from tile import Tile
from player import Player


class Level():
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = None
        self.setup_map()

    def setup_map(self):
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
        self.visible_sprites.calculate_offset(self.player)
        self.visible_sprites.draw_floor(self.player)
        self.visible_sprites.draw_sprites(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        # Camera attributes
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(0, 0)

        # Floor attributes
        self.floor_surface = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def calculate_offset(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

    def draw_floor(self, player):
        offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, offset_pos)

    def draw_sprites(self, player):
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
