import pygame
from typing import Union

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: Union[tuple[int, int], pygame.math.Vector2], *groups: Union[pygame.sprite.Group, list[pygame.sprite.Group]]) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load('../graphics/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)