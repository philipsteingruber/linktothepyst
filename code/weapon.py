from typing import Union

import pygame

from player import Player
from timer import Timer


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: Player, groups: Union[pygame.sprite.Group, list[pygame.sprite.Group]]) -> None:
        super().__init__(groups)
        self.player = player
        self.direction = self.player.status.split('_')[0]

        self.sprite_type = 'weapon'

        self.lifetime = Timer(400, self.kill)
        self.lifetime.activate()

        self.image = pygame.image.load(f'../graphics/weapons/{self.player.equipped_weapon}/{self.direction}.png').convert_alpha()

        if self.direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft)
            self.rect.y += 16
        elif self.direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright)
            self.rect.y += 16
        if self.direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop)
            self.rect.x -= 10
        if self.direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom)
            self.rect.x -= 10

    def update(self):
        self.lifetime.update()
