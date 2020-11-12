import pygame
import os

def load_images(folder, files):
    return [load_image(folder, file) for file in files]

def load_image(folder, file):
    return pygame.image.load(os.path.join(folder, file))

def scale_image(image, width, height):
    return pygame.transform.scale(image, (width, height))

def rotate_image(image, amount):
    return pygame.transform.rotate(image, amount)
