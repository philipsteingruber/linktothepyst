import random

import pygame
from enemy import Enemy
from player import Player
from settings import TILESIZE
from support import import_images_from_folder, import_layout_from_csv
from tile import Tile
from ui import UI
from weapon import Weapon
from particles import ParticleAnimationPlayer
from debug import debug


class Level():
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Attack sprites
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Player and Map
        self.player = None
        self.setup_map_and_player()

        # UI
        self.ui = UI()

        # Particles
        self.particle_player = ParticleAnimationPlayer()

    def setup_map_and_player(self):
        layouts = {
            'boundary': import_layout_from_csv('../map/map_floorblocks.csv'),
            'grass': import_layout_from_csv('../map/map_grass.csv'),
            'object': import_layout_from_csv('../map/map_objects.csv'),
            'entities': import_layout_from_csv('../map/map_Entities.csv')
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
                            Tile(pos=(x, y), groups=[self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], surface=random.choice(graphics['grass']), sprite_type='grass')
                        if style == 'object':
                            Tile(pos=(x, y), groups=[self.visible_sprites, self.obstacle_sprites], surface=graphics['objects'][int(cell)], sprite_type='object')
                        if style == 'entities':
                            if cell == '394':
                                self.player = Player(pos=(x, y),
                                                     groups=self.visible_sprites,
                                                     obstacle_sprites=self.obstacle_sprites,
                                                     create_attack=self.create_attack,
                                                     create_magic=self.create_magic)
                            else:
                                if cell == '390':
                                    enemy_type = 'bamboo'
                                if cell == '391':
                                    enemy_type = 'spirit'
                                if cell == '392':
                                    enemy_type = 'raccoon'
                                if cell == '393':
                                    enemy_type = 'squid'
                                Enemy(groups=[self.visible_sprites, self.attackable_sprites], enemy_type=enemy_type, pos=(x, y), obstacle_sprites=self.obstacle_sprites, damage_player=self.damage_player)

    def create_attack(self):
        Weapon(player=self.player, groups=[self.visible_sprites, self.attack_sprites])

    def create_magic(self, magic_type, strength, cost):
        print(f'Using magic: {magic_type} - {strength} - {cost}')

    def damage_player(self, amount: int, attack_type: str) -> None:
        if self.player.attackable:
            self.player.take_damage(amount)
            self.particle_player.create_particles(pos=self.player.rect.center, groups=[self.visible_sprites], particle_type=attack_type)

    def player_attack(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites.sprites():
                colliding_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if colliding_sprites:
                    for colliding_sprite in colliding_sprites:
                        sprite_type = colliding_sprite.sprite_type
                        if sprite_type == 'grass':
                            offset = pygame.math.Vector2(0, 50)
                            for _ in range(random.randint(3, 6)):
                                self.particle_player.create_particles(pos=colliding_sprite.rect.center - offset, groups=[self.visible_sprites], particle_type='leaf')
                            colliding_sprite.kill()
                        if sprite_type == 'enemy':
                            enemy = colliding_sprite
                            enemy.take_damage(player=self.player, attack_type=attack_sprite.sprite_type)
                            if enemy.health <= 0:
                                self.particle_player.create_particles(pos=enemy.rect.center, groups=[self.visible_sprites], particle_type=enemy.enemy_type)
                                enemy.kill()

    def run(self):
        self.visible_sprites.calculate_offset(self.player)
        self.visible_sprites.draw_floor(self.player)
        self.visible_sprites.draw_sprites(self.player)
        self.visible_sprites.update()
        self.visible_sprites.update_enemies(self.player)
        self.player_attack()
        self.ui.display(self.player)
        debug(self.player.attackable)


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

    def update_enemies(self, player: Player):
        enemy_sprites = [sprite for sprite in self.sprites() if sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player=player)
