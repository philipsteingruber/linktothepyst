from typing import Union

import pygame
from settings import TILESIZE


class Tile(pygame.sprite.Sprite):

    def __init__(self, pos: Union[tuple[int, int], pygame.math.Vector2],
                 groups: Union[pygame.sprite.Group, list[pygame.sprite.Group]],
                 sprite_type: str,
                 surface: pygame.Surface = pygame.Surface((TILESIZE, TILESIZE))) -> None:

        super().__init__(groups)

        self.sprite_type = sprite_type
        self.image = surface

        if self.sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.copy().inflate(0, -10)
