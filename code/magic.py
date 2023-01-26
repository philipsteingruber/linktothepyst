import pygame
from player import Player
from settings import TILESIZE
import random


class MagicCaster:
    def __init__(self, animation_player) -> None:
        self.animation_player = animation_player

    def heal(self, player: Player, strength: int, cost: int, groups: list[pygame.sprite.Group]) -> None:
        max_health = player.stats['health']
        if player.current_energy >= cost and player.current_health < max_health:
            player.current_health += strength
            if player.current_health > max_health:
                player.current_health = max_health
            player.current_energy -= cost
            self.animation_player.create_particles(pos=player.rect.center - pygame.math.Vector2(0, 60), groups=groups, particle_type='heal')
            self.animation_player.create_particles(pos=player.rect.center, groups=groups, particle_type='aura')

    def flame(self, player: Player, cost: int, groups: list[pygame.sprite.Group]):
        if player.current_energy >= cost:
            player.current_energy -= cost

            player_direction = player.status.split('_')[0]
            if player_direction == 'right':
                spell_direction = pygame.math.Vector2(1, 0)
            elif player_direction == 'left':
                spell_direction = pygame.math.Vector2(-1, 0)
            elif player_direction == 'up':
                spell_direction = pygame.math.Vector2(0, -1)
            else:
                spell_direction = pygame.math.Vector2(0, 1)

            for offset_index in range(1, 6):
                offset = spell_direction * offset_index * TILESIZE + pygame.math.Vector2(random.randint(-(TILESIZE // 5), (TILESIZE // 5)))
                self.animation_player.create_particles(particle_type='flame', pos=player.rect.center + offset, groups=groups)
