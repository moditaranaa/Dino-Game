# main.py

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE
from dino import Dino
from obstacle import Cactus
from background import Background

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dino Scooter Game")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 72)

    # High score tracker
    high_score = 0

    # GAME LOOP (with replay)
    while True:
        # Reset everything at game start
        all_sprites = pygame.sprite.Group()
        cactus_group = pygame.sprite.Group()

        dino = Dino()
        background = Background("assets/background/desert_background.jpg", speed=4)
        all_sprites.add(dino)

        SPAWN_CACTUS = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_CACTUS, 1500)

        score = 0
        running = True
        game_over = False

        # Main match loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == SPAWN_CACTUS:
                    cactus = Cactus()
                    cactus_group.add(cactus)

            # Update
            background.update()
            all_sprites.update()
            cactus_group.update()

            # Collision check
            if not game_over and pygame.sprite.spritecollideany(dino, cactus_group):
                dino.image = dino.dead_img
                game_over = True
                pygame.mixer.music.stop()
                # Optional crash sound here

            # Draw everything
            background.draw(screen)
            all_sprites.draw(screen)
            cactus_group.draw(screen)

            # Show score
            if not game_over:
                score += 1
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

            # Game Over Screen
            if game_over:
                if score > high_score:
                    high_score = score

                game_over_text = big_font.render("Game Over", True, (255, 0, 0))
                restart_text = font.render("Press R to Restart or Q to Quit", True, (0, 0, 0))
                hs_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))

                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 60))
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 + 10))
                screen.blit(hs_text, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 50))

                pygame.display.flip()

                # Pause and wait for keypress
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                waiting = False  # restart
                                running = False
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()
                    clock.tick(FPS)
                break

            pygame.display.update()
            clock.tick(FPS)

if __name__ == "__main__":
    main()