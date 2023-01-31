import pygame
from player import Player
from settings import UI_FONT, UI_FONT_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, UI_BG_COLOR, TEXT_COLOR, TEXT_COLOR_SELECTED, UI_BORDER_COLOR, UI_BORDER_COLOR_ACTIVE, UPGRADE_BG_COLOR_SELECTED
from settings import BAR_COLOR, BAR_COLOR_SELECTED
from timer import Timer


class UpgradeMenu:
    def __init__(self, player: Player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Menu interaction
        self.selected_index = 0
        self.max_index = len(self.player.stats) - 1
        self.stat_names = list(self.player.stats.keys())
        self.switched_selection = Timer(200)
        self.upgraded_stat = Timer(200)

        # Menu item dimensions
        self.number_of_menu_items = len(self.player.stats)
        self.menu_item_height = SCREEN_HEIGHT * 0.8
        self.menu_item_width = SCREEN_WIDTH // (self.number_of_menu_items + 1)
        self.menu_items = self.create_menu_items()

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.switched_selection.active:
            if keys[pygame.K_LEFT]:
                self.selected_index -= 1
                if self.selected_index < 0:
                    self.selected_index = self.max_index
                self.switched_selection.activate()
            elif keys[pygame.K_RIGHT]:
                self.selected_index += 1
                if self.selected_index > self.max_index:
                    self.selected_index = 0
                self.switched_selection.activate()
            elif keys[pygame.K_SPACE] and not self.upgraded_stat.active:
                self.menu_items[self.selected_index].upgrade(self.player)
                self.upgraded_stat.activate()

    def display(self):
        self.switched_selection.update()
        self.upgraded_stat.update()

        self.input()
        for index, menu_item in enumerate(self.menu_items):
            name = self.stat_names[index]
            value = self.player.stats[name]
            max_value = self.player.max_stats[name]
            cost = self.player.upgrade_cost[name]
            menu_item.display(selected_index=self.selected_index, stat_name=name.title(), stat_value=value, max_value=max_value, upgrade_cost=cost)

    def create_menu_items(self):
        item_list = []

        for i in range(self.number_of_menu_items):
            padding = SCREEN_WIDTH // self.number_of_menu_items
            left = padding * i + (padding - self.menu_item_width) // 2
            top = SCREEN_WIDTH * 0.1

            item_list.append(MenuItem(left=left, top=top, width=self.menu_item_width, height=self.menu_item_height, index=i, font=self.font))
        return item_list


class MenuItem:
    def __init__(self, left: int, top: int, width: int, height: int, index: int, font: pygame.font.Font) -> None:
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

        self.display_surface = pygame.display.get_surface()

    def upgrade(self, player):
        attribute_to_upgrade = list(player.stats.keys())[self.index]
        upgrade_cost = player.upgrade_cost[attribute_to_upgrade]

        if player.current_xp >= upgrade_cost and player.stats[attribute_to_upgrade] < player.max_stats[attribute_to_upgrade]:
            player.current_xp -= upgrade_cost
            player.stats[attribute_to_upgrade] *= 1.2
            player.upgrade_cost[attribute_to_upgrade] *= 1.4
            if player.stats[attribute_to_upgrade] > player.max_stats[attribute_to_upgrade]:
                player.stats[attribute_to_upgrade] = player.max_stats[attribute_to_upgrade]

    def display_background(self, selected: bool) -> None:
        if selected:
            pygame.draw.rect(self.display_surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, self.rect, 4)
        else:
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.rect, 4)

    def display_text(self, stat_name: str, upgrade_cost: int, selected: bool) -> None:
        if selected:
            color = TEXT_COLOR_SELECTED
        else:
            color = TEXT_COLOR
        # Title
        title_surface: pygame.Surface = self.font.render(stat_name, False, color)
        title_rect = title_surface.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))
        self.display_surface.blit(title_surface, title_rect)

        # Cost
        cost_surface: pygame.Surface = self.font.render(f'Upgrade - {int(upgrade_cost)}', False, color)
        cost_rect: pygame.Rect = cost_surface.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))
        self.display_surface.blit(cost_surface, cost_rect)

    def display_bar(self, stat_value: int, max_value: int, selected: bool):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        if selected:
            color = BAR_COLOR_SELECTED
        else:
            color = BAR_COLOR

        full_height = bottom[1] - top[1]
        allocated_ratio = stat_value / max_value * full_height
        allocated_rect = pygame.Rect(top[0] - 15, bottom[1] - allocated_ratio, 30, 10)

        pygame.draw.line(self.display_surface, color, top, bottom, 5)
        pygame.draw.rect(self.display_surface, color, allocated_rect)

    def display(self, selected_index: int, stat_name: str, stat_value: int, max_value: int, upgrade_cost: int):
        self.display_background(selected=self.index == selected_index)
        self.display_text(stat_name=stat_name, upgrade_cost=upgrade_cost, selected=self.index == selected_index)
        self.display_bar(stat_value, max_value, selected=self.index == selected_index)
