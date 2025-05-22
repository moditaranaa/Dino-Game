import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE
from dino import Dino
from obstacle import Cactus
from background import Background

def start_screen(screen, font, big_font):
    # Load background + dino
    background = pygame.image.load("assets/background/desert_background.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    blur_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    blur_overlay.set_alpha(120)
    blur_overlay.fill((255, 255, 255))

    dino_img = pygame.image.load("assets/dino/dino_jump.png").convert_alpha()
    dino_img = pygame.transform.scale(dino_img, (120, 120))

    title = big_font.render("Dino Game", True, (0, 128, 255))
    subtext = font.render("Press ENTER to start. Thank you for watching.", True, (0, 0, 0))

    # Centered positions
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    subtext_rect = subtext.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    dino_rect = dino_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))

    name = ""
    input_font = pygame.font.SysFont(None, 32)

    active_typing = True
    while active_typing:
        screen.blit(background, (0, 0))
        screen.blit(blur_overlay, (0, 0))
        screen.blit(title, title_rect)
        screen.blit(subtext, subtext_rect)
        screen.blit(dino_img, dino_rect)

        # Name input
        name_prompt = font.render("Enter your name:", True, (0, 0, 0))
        screen.blit(name_prompt, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60))
        name_surface = input_font.render(name, True, (0, 100, 255))
        screen.blit(name_surface, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    active_typing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15:
                        name += event.unicode
    return name

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dino Scooter Game")
    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 72)
    clock = pygame.time.Clock()

    # Show start screen + name input
    player_name = start_screen(screen, font, big_font)

    high_score = 0

    while True:
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
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                if event.type == SPAWN_CACTUS and not paused and not game_over:
                    cactus = Cactus()
                    cactus_group.add(cactus)

            if not paused and not game_over:
                background.update()
                all_sprites.update()
                cactus_group.update()

                if pygame.sprite.spritecollideany(dino, cactus_group):
                    dino.image = dino.dead_img
                    game_over = True
                    pygame.mixer.music.stop()

            # Draw
            background.draw(screen)
            all_sprites.draw(screen)
            cactus_group.draw(screen)

            if not paused and not game_over:
                score += 1

            # 🟦 Transparent Score: Left + Right
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (20, 20))
            high_text = font.render(f"High: {high_score}", True, (80, 80, 80))
            screen.blit(high_text, (SCREEN_WIDTH - 150, 20))

            if paused and not game_over:
                pause_overlay = big_font.render("PAUSED", True, (200, 0, 200))
                screen.blit(pause_overlay, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

            if game_over:
                if score > high_score:
                    high_score = score

                game_over_text = big_font.render("Game Over", True, (255, 0, 0))
                restart_text = font.render("Press R to Restart or Q to Quit", True, (0, 0, 0))
                name_text = font.render(f"{player_name}'s Score: {score}", True, (0, 0, 0))
                hs_display = font.render(f"High Score: {high_score}", True, (0, 0, 0))

                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 60))
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 + 10))
                screen.blit(name_text, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50))
                screen.blit(hs_display, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 90))

                pygame.display.flip()

                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                waiting = False
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