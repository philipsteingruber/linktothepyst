import random

import pygame
from debug import debug
from player import Player
from settings import TILESIZE
from support import import_images_from_folder, import_layout_from_csv
from tile import Tile
from ui import UI
from weapon import Weapon


class Level():
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = None
        self.setup_map_and_player()

        # UI
        self.ui = UI()

    def setup_map_and_player(self):
        layouts = {
            'boundary': import_layout_from_csv('../map/map_floorblocks.csv'),
            'grass': import_layout_from_csv('../map/map_grass.csv'),
            'object': import_layout_from_csv('../map/map_objects.csv'),
        }
        graphics = {
            'grass': import_images_from_folder('../graphics/grass'),
            'objects': import_images_from_folder('../graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    if cell != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile(pos=(x, y), groups=[self.obstacle_sprites], sprite_type='invisible')
                        if style == 'grass':
                            Tile(pos=(x, y), groups=[self.visible_sprites, self.obstacle_sprites], surface=random.choice(graphics['grass']), sprite_type='grass')
                        if style == 'object':
                            # pass
                            Tile(pos=(x, y), groups=[self.visible_sprites, self.obstacle_sprites], surface=graphics['objects'][int(cell)], sprite_type='object')

        self.player = Player(pos=(2000, 1430),
                             groups=self.visible_sprites,
                             obstacle_sprites=self.obstacle_sprites,
                             create_attack=self.create_attack,
                             create_magic=self.create_magic)

    def create_attack(self):
        Weapon(player=self.player, groups=self.visible_sprites)

    def create_magic(self, magic_type, strength, cost):
        print(f'Using magic: {magic_type} - {strength} - {cost}')

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.calculate_offset(self.player)
        self.visible_sprites.draw_floor(self.player)
        self.visible_sprites.draw_sprites(self.player)
        self.ui.display(self.player)


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
