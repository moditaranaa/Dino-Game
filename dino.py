# dino.py

import pygame
from config import GROUND_Y

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load all the dino sprites
        self.idle_img = pygame.transform.scale(
            pygame.image.load("assets/dino/dino_idle.png").convert_alpha(), (60, 60))
        self.jump_img = pygame.transform.scale(
            pygame.image.load("assets/dino/dino_jump.png").convert_alpha(), (60, 60))
        self.land_img = pygame.transform.scale(
            pygame.image.load("assets/dino/dino_land.png").convert_alpha(), (60, 60))
        self.dead_img = pygame.transform.scale(
            pygame.image.load("assets/dino/dino_dead.png").convert_alpha(), (60, 60))

        self.image = self.idle_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_Y - self.rect.height

        # Physics values
        self.velocity = 0
        self.gravity = 1
        self.jump_power = -15
        self.is_jumping = False

        # Load jump sound
        try:
            self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
        except:
            self.jump_sound = None

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity = self.jump_power
            self.is_jumping = True
            self.image = self.jump_img

            # Play jump sound (safely)
            if self.jump_sound:
                self.jump_sound.play()

        # Gravity and motion
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # When Dino lands back on ground
        if self.rect.y >= GROUND_Y - self.rect.height:
            self.rect.y = GROUND_Y - self.rect.height
            self.velocity = 0
            if self.is_jumping:
                self.image = self.land_img
            else:
                self.image = self.idle_img
            self.is_jumping = False

        # Mid-air fall appearance
        elif self.velocity > 0:
            self.image = self.land_img