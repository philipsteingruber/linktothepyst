import math
from typing import Union

import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: Union[pygame.sprite.Group, list[pygame.sprite.Group]]) -> None:
        super().__init__(groups)

        self.rect = None
        self.hitbox = None
        self.obstacle_sprites = None

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

        self.sprite_type = 'entity'

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def get_flicker_alpha(self) -> int:
        value = math.sin(pygame.time.get_ticks())
        return int(math.fabs(value) * 255)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
