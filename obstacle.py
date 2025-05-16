# obstacle.py

import pygame
import random
from config import GROUND_Y

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load all cactus images
        cactus_imgs = [
            "assets/obstacles/cactus.png",
            "assets/obstacles/pink_cactus.png",
            "assets/obstacles/orange_cactus.png",
            "assets/obstacles/yellow_cactus.png"
        ]
        selected = random.choice(cactus_imgs)
        self.image = pygame.image.load(selected).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 60))  # Resize to look cute and fair

        self.rect = self.image.get_rect()
        self.rect.x = 800  # Start from right edge
        self.rect.y = GROUND_Y - self.rect.height

        self.speed = 10

    def update(self):
        self.rect.x -= self.speed

        # Remove cactus if it goes off screen
        if self.rect.right < 0:
            self.kill()