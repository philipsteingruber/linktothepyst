import pygame

from player import Player
from settings import HEALTH_COLOR, ENERGY_COLOR, UI_BG_COLOR, UI_BORDER_COLOR, UI_BORDER_COLOR_ACTIVE, WEAPON_DATA, MAGIC_DATA
from settings import UI_FONT, UI_FONT_SIZE, HEALTH_BAR_WIDTH, BAR_HEIGHT, ENERGY_BAR_WIDTH, SCREEN_WIDTH, ITEM_BOX_SIZE


class UI:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Health / Energy
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Convert weapon data
        self.weapon_graphics = []
        for weapon in WEAPON_DATA.values():
            path = weapon['graphic']
            self.weapon_graphics.append(pygame.image.load(path).convert_alpha())

        # Convert magic data
        self.magic_graphics = []
        for magic in MAGIC_DATA.values():
            path = magic['graphic']
            self.magic_graphics.append(pygame.image.load(path).convert_alpha())

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        # Draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Draw the bar
        bar_rect = bg_rect.copy()
        bar_rect.width *= (current_amount / max_amount)
        pygame.draw.rect(self.display_surface, color, bar_rect)

        # Draw the border
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_xp(self, current_exp):
        text_surf = self.font.render(f'EXPERIENCE - {int(current_exp)}', False, 'black')
        text_rect = text_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20))

        # Draw background
        bg_rect = text_rect.copy().inflate(20, 20)
        pygame.draw.rect(self.display_surface, 'white', bg_rect)

        # Draw border
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        # Draw text
        self.display_surface.blit(text_surf, text_rect)

    def get_and_draw_equipment_box(self, left: int, top: int, player: Player, equipment_type: str) -> pygame.Rect:
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if player.timers[f'switching_{equipment_type}'].active:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def display_weapon_overlay(self, left, top, player):
        bg_rect = self.get_and_draw_equipment_box(left=left, top=top, player=player, equipment_type='weapon')
        weapon_surf = self.weapon_graphics[player.weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def display_magic_overlay(self, left, top, player):
        bg_rect = self.get_and_draw_equipment_box(left=left, top=top, player=player, equipment_type='magic')
        magic_surf = self.magic_graphics[player.magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player: Player) -> None:
        # Health/energy bars
        self.show_bar(player.current_health, player.stats['max_health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.current_energy, player.stats['max_energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_xp(player.current_xp)

        self.display_weapon_overlay(left=10, top=630, player=player)
        self.display_magic_overlay(left=95, top=630, player=player)
        # Magic overlay
        # self.selection_box(95, 630)
