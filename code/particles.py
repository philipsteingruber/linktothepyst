import pygame
from support import import_images_from_folder
from typing import Union
import random


class ParticleAnimationPlayer:
    def __init__(self) -> None:
        self.frames = {
            # magic
            'flame': import_images_from_folder('../graphics/particles/flame/frames'),
            'aura': import_images_from_folder('../graphics/particles/aura'),
            'heal': import_images_from_folder('../graphics/particles/heal/frames'),

            # attacks
            'claw': import_images_from_folder('../graphics/particles/claw'),
            'slash': import_images_from_folder('../graphics/particles/slash'),
            'sparkle': import_images_from_folder('../graphics/particles/sparkle'),
            'leaf_attack': import_images_from_folder('../graphics/particles/leaf_attack'),
            'thunder': import_images_from_folder('../graphics/particles/thunder'),

            # monster deaths
            'squid': import_images_from_folder('../graphics/particles/smoke_orange'),
            'raccoon': import_images_from_folder('../graphics/particles/raccoon'),
            'spirit': import_images_from_folder('../graphics/particles/nova'),
            'bamboo': import_images_from_folder('../graphics/particles/bamboo'),

            # leaves
            'leaf': (
                import_images_from_folder('../graphics/particles/leaf1'),
                import_images_from_folder('../graphics/particles/leaf2'),
                import_images_from_folder('../graphics/particles/leaf3'),
                import_images_from_folder('../graphics/particles/leaf4'),
                import_images_from_folder('../graphics/particles/leaf5'),
                import_images_from_folder('../graphics/particles/leaf6'),
                self.flip_frames(import_images_from_folder('../graphics/particles/leaf1')),
                self.flip_frames(import_images_from_folder('../graphics/particles/leaf2')),
                self.flip_frames(import_images_from_folder('../graphics/particles/leaf3')),
                self.flip_frames(import_images_from_folder('../graphics/particles/leaf4')),
                self.flip_frames(import_images_from_folder('../graphics/particles/leaf5')),
                self.flip_frames(import_images_from_folder('../graphics/particles/leaf6'))
            )
        }

    def flip_frames(self, frames: list[pygame.Surface]) -> pygame.Surface:
        flipped_frames = []
        for frame in frames:
            flipped_frames.append(pygame.transform.flip(surface=frame, flip_x=True, flip_y=False))
        return flipped_frames

    def create_particles(self, pos: tuple[int, int], groups: list[pygame.sprite.Group], particle_type: str) -> None:
        if particle_type == 'leaf':
            animation_frames = random.choice(self.frames['leaf'])
        else:
            animation_frames = self.frames[particle_type]
        ParticleEffect(pos=pos, groups=groups, animation_frames=animation_frames)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, groups: Union[pygame.sprite.Group, list[pygame.sprite.Group]], pos: tuple[int, int], animation_frames: list[pygame.Surface]) -> None:
        super().__init__(groups)

        self.animation_frames = animation_frames
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.sprite_type = 'particle'

    def animate(self) -> None:
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_frames):
            self.kill()
        else:
            self.image = self.animation_frames[int(self.frame_index)]

    def update(self) -> None:
        self.animate()
