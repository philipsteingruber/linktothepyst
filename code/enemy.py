from typing import Union, Callable

import pygame
from entity import Entity
from player import Player
from settings import MONSTER_DATA
from support import import_images_from_folder
from timer import Timer


class Enemy(Entity):
    def __init__(self, groups: Union[pygame.sprite.Group, list[pygame.sprite.Group]], enemy_type: str, pos: tuple[int, int], obstacle_sprites: pygame.sprite.Group, damage_player: Callable) -> None:
        super().__init__(groups)

        # General Setup
        self.enemy_type = enemy_type
        self.sprite_type = 'enemy'

        # Graphics
        self.animations = self.import_graphics(enemy_type=self.enemy_type)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # Movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Stats
        enemy_info = MONSTER_DATA[self.enemy_type]
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.weight = enemy_info['weight']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']

        # Player interaction
        self.timers = []
        self.can_attack = True
        self.attack_timer = Timer(400, self.allow_attack)
        self.damage_taken_timer = Timer(400)
        self.damage_player = damage_player

    def import_graphics(self, enemy_type: str) -> dict[str: list[pygame.Surface]]:
        animations = {'idle': [], 'move': [], 'attack': []}
        top_folder = f'../graphics/monsters/{enemy_type}/'
        for animation in animations:
            animations[animation] = import_images_from_folder(top_folder + animation)
        return animations

    def get_player_distance(self, player: Player) -> float:
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        return (player_vec - enemy_vec).magnitude()

    def get_player_direction(self, player: Player) -> pygame.math.Vector2:
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        result_vec = enemy_vec - player_vec
        if result_vec.magnitude() != 0:
            return (player_vec - enemy_vec).normalize()
        else:
            return pygame.math.Vector2()

    def take_damage(self, amount: int) -> None:
        if not self.damage_taken_timer.active:
            self.health -= amount
            self.damage_taken_timer.activate()

    def hit_reaction(self):
        if self.damage_taken_timer.active:
            self.direction *= -self.weight

    def allow_attack(self):
        self.can_attack = True

    def set_status(self, player: Player) -> None:
        distance = self.get_player_distance(player=player)

        if distance <= self.attack_radius and not self.attack_timer.active:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def take_actions(self, player: Player) -> None:
        if self.status == 'attack':
            self.damage_player(self.attack_damage, self.attack_type)
        if self.status == 'move':
            self.direction = self.get_player_direction(player=player)
        else:
            self.direction = pygame.math.Vector2()

    def animate(self) -> None:
        # TODO: Attack-animationer är trasiga
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
            if self.status == 'attack':
                self.attack_timer.activate()
        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if self.damage_taken_timer.active:
            self.image.set_alpha(self.get_flicker_alpha())
        else:
            self.image.set_alpha(255)

    def update(self) -> None:
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.attack_timer.update()
        self.damage_taken_timer.update()

    def enemy_update(self, player: Player):
        self.set_status(player=player)
        self.take_actions(player=player)
