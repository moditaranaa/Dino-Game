# background.py

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Background:
    def __init__(self, image_path, speed=5):
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.speed = speed
        self.x1 = 0
        self.x2 = self.image.get_width()

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        # Reset images when they scroll off screen
        if self.x1 <= -self.image.get_width():
            self.x1 = self.image.get_width()

        if self.x2 <= -self.image.get_width():
            self.x2 = self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))