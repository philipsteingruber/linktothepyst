from typing import Union, Callable

import pygame
from settings import WEAPON_DATA, MAGIC_DATA
from support import import_images_from_folder
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: Union[tuple[int, int], pygame.math.Vector2],
                 groups: Union[pygame.sprite.Group, list[pygame.sprite.Group]],
                 obstacle_sprites: pygame.sprite.Group, create_attack: Callable,
                 create_magic: Callable) -> None:
        # Sprite setup
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # Collision attributes
        self.hitbox = self.rect.copy().inflate(0, -26)
        self.obstacle_sprites = obstacle_sprites

        # Movement attributes
        self.direction = pygame.math.Vector2(0, 0)

        # Timers
        self.timers = {
            'attacking': Timer(400),
            'switching_weapon': Timer(200),
            'switching_magic': Timer(200),
        }

        # Animations
        self.animations = self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.update_animation_frame()

        # Weapon
        self.create_attack = create_attack
        self.weapon_index = 0
        self.equipped_weapon = list(WEAPON_DATA.keys())[self.weapon_index]

        # Magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.equipped_magic = list(MAGIC_DATA.keys())[self.magic_index]

        # Stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.current_health = self.stats['health']
        self.current_energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.current_xp = 0

    def import_player_assets(self) -> dict[str: list[pygame.Surface]]:
        path = '../graphics/player/'

        animations = {'up': [], 'down': [], 'left': [], 'right': [],
                      'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                      'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in animations:
            animations[animation] = import_images_from_folder(path + animation)
        return animations

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['attacking'].active:
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE]:
                self.timers['attacking'].activate()
                self.create_attack()

            if keys[pygame.K_LCTRL]:
                self.timers['attacking'].activate()
                self.create_magic(magic_type=self.equipped_magic,
                                  strength=MAGIC_DATA[self.equipped_magic]['strength'] + self.stats['magic'],
                                  cost=MAGIC_DATA[self.equipped_magic]['cost'])

            if keys[pygame.K_q] and not self.timers['switching_weapon'].active:
                self.weapon_index += 1
                if self.weapon_index >= len(WEAPON_DATA.keys()):
                    self.weapon_index = 0
                self.equipped_weapon = list(WEAPON_DATA.keys())[self.weapon_index]
                self.timers['switching_weapon'].activate()

            if keys[pygame.K_w] and not self.timers['switching_magic'].active:
                self.magic_index += 1
                if self.magic_index >= len(MAGIC_DATA.keys()):
                    self.magic_index = 0
                self.equipped_magic = list(MAGIC_DATA.keys())[self.magic_index]
                self.timers['switching_magic'].activate()

    def set_status(self):
        if self.direction.magnitude() == 0 and not self.timers['attacking'].active:
            self.status = self.status.split('_')[0] + '_idle'
        if self.timers['attacking'].active:
            self.status = self.status.split('_')[0] + '_attack'

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index = (self.frame_index + self.animation_speed) % len(animation)
        self.image = self.update_animation_frame()
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update_animation_frame(self):
        return self.animations[self.status][int(self.frame_index)]

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

    def update(self):
        for timer in self.timers.values():
            timer.update()
        self.input()
        self.move(self.speed)
        self.set_status()
        self.animate()
