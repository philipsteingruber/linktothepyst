import csv
import os

import pygame


def import_layout_from_csv(path: str) -> list[str]:
    map_list = []
    with open(path) as level_map:
        reader = csv.reader(level_map, delimiter=',')
        for row in reader:
            map_list.append(list(row))
    return map_list


def import_images_from_folder(path: str) -> list[pygame.Surface]:
    images = []
    for _, __, file_names in os.walk(path):
        for file_name in file_names:
            images.append(pygame.image.load(path + '/' + file_name).convert_alpha())
    return images
