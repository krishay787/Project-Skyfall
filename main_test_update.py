import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Skyfall')
clock = pygame.time.Clock()
font = pygame.font.Font('Font\\Pixelon.ttf', 100)
small_font = pygame.font.Font(None, 36)

# Game states
game_state = 'menu'

# Colors
SKY_COLOR = '#cef1f9'
OVERLAY_COLOR = '#80e8ff'
BRICK_RED = (178, 34, 34)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Assets
text_surf = font.render('Skyfall', False, ('#c55b56'))
text_rect = text_surf.get_rect(center=(400, 150))

game_over_text = font.render('Game Over', False, ('#c55b56'))
game_over_rect = game_over_text.get_rect(center=(400, 150))

main_menu_text = small_font.render("Click to return to Main Menu", True, (WHITE))
main_menu_text_rect = main_menu_text.get_rect(center=(400, 300))



cloud_surf = pygame.image.load('Graphics\cloud.png').convert_alpha()
cloud_surf = pygame.transform.scale(cloud_surf, (155, 93))
cloud_rect = cloud_surf.get_rect(center=(260, 160))
cloud_rect_2 = cloud_surf.get_rect(center=(550, 120))

cloud_surf_2 = pygame.transform.scale(cloud_surf, (126, 76))
cloud_rect_3 = cloud_surf_2.get_rect(topleft=(120, 448))
cloud_rect_4 = cloud_surf_2.get_rect(topleft=(545, 480))

overlay_shape = pygame.surface.Surface((774, 568))
overlay_rect = overlay_shape.get_rect(center=(400, 300))

play_btn = pygame.image.load('Graphics\playbutton.png').convert_alpha()
play_btn_rect = play_btn.get_rect(topleft=(185, 260))

shop_btn = pygame.image.load('Graphics\shopbutton.png').convert_alpha()
shop_btn_rect = shop_btn.get_rect(topleft=(438, 260))

highscore_panel = pygame.image.load('Graphics\highscorepanel.png').convert_alpha()
highscore_panel_rect = highscore_panel.get_rect(topleft=(193, 358))

mapchooser = pygame.image.load('Graphics\map_panel.png').convert_alpha()
mapchooser_rect = mapchooser.get_rect(center=(400, 300))

classic_btn = pygame.image.load('Graphics\classic_btn.png').convert_alpha()
classic_btn_rect = classic_btn.get_rect(center=(220, 260))

space_btn = pygame.image.load('Graphics\space_btn.png').convert_alpha()
space_btn_rect = space_btn.get_rect(center=(350, 260))

# storm_btn = pygame.image.load('Graphics\storm_btn.png').convert_alpha()
# storm_btn_rect = storm_btn.get_rect(center=(500, 260))


# Gameplay variables
player = pygame.Rect(400 - 25, 520, 50, 50)
player_speed = 7
blocks = []
block_speed = 6
abilities = []
ability_speed = 4
spawn_timer = 0
invincible = False
break_blocks = False
invincible_timer = 0
break_timer = 0
INVINCIBLE_DURATION = 300
BREAK_DURATION = 180
score = 0

def reset_game():
    global player, blocks, abilities, invincible, break_blocks, invincible_timer, break_timer, spawn_timer, score
    player = pygame.Rect(400 - 25, 520, 50, 50)
    blocks = []
    abilities = []
    invincible = False
    break_blocks = False
    invincible_timer = 0
    break_timer = 0
    spawn_timer = 0
    score = 0

def spawn_block():
    x = random.randint(0, 740)
    blocks.append(pygame.Rect(x, -30, 60, 30))

def spawn_ability():
    x = random.randint(0, 770)
    ability_type = random.choice(["invincible", "break"])
    abilities.append({"rect": pygame.Rect(x, -30, 30, 30), "type": ability_type})

def update_block_speed(score):
    base_speed = 6
    max_speed = 50
    increment = score // 500
    return min(base_speed + increment, max_speed)


# Main game loop
while True:

    # Menu screen
    if game_state == 'menu':
        screen.fill(SKY_COLOR)
        pygame.draw.rect(screen, OVERLAY_COLOR, overlay_rect, 500, border_radius=15)
        screen.blit(cloud_surf, cloud_rect)
        screen.blit(cloud_surf, cloud_rect_2)
        screen.blit(text_surf, text_rect)
        screen.blit(play_btn, play_btn_rect)
        screen.blit(shop_btn, shop_btn_rect)
        screen.blit(highscore_panel, highscore_panel_rect)
        screen.blit(cloud_surf_2, cloud_rect_3)
        screen.blit(cloud_surf_2, cloud_rect_4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Navigation to different screens
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_btn_rect.collidepoint(event.pos):
                    game_state = 'choosing'
                elif shop_btn_rect.collidepoint(event.pos):
                    game_state = 'shop'

    # ========================= GAMEPLAY ============================
    elif game_state == 'choosing':
        screen.blit(mapchooser, mapchooser_rect)
        screen.blit(classic_btn, classic_btn_rect)
        # screen.blit(space_btn, space_btn_rect)
        # screen.blit(storm_btn, storm_btn_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if classic_btn_rect.collidepoint(event.pos):
                    reset_game()
                    game_state = 'playing1'

    elif game_state == 'game_over':
        screen.blit(game_over_text, game_over_rect)
        screen.blit(main_menu_text, main_menu_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_state = 'menu'

    elif game_state == 'playing1':

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < 800:
            player.x += player_speed

        spawn_timer += 1
        score += 1  # score increases as time passes
        block_speed = update_block_speed(score)

        if spawn_timer % 40 == 0:
            spawn_block()
        if spawn_timer % 250 == 0:
            spawn_ability()

        # Timers
        if invincible:
            invincible_timer -= 1
            if invincible_timer <= 0:
                invincible = False
        if break_blocks:
            break_timer -= 1
            if break_timer <= 0:
                break_blocks = False

        # Move blocks
        for block in blocks[:]:
            block.y += block_speed
            if block.top > 600:
                blocks.remove(block)
            elif block.colliderect(player):
                if break_blocks:
                    blocks.remove(block)
                elif not invincible:
                    game_state = 'game_over' # ADD GAME OVER LOGIC HERE

        # Move abilities
        for ability in abilities[:]:
            ability["rect"].y += ability_speed
            if ability["rect"].top > 600:
                abilities.remove(ability)
            elif ability["rect"].colliderect(player):
                if ability["type"] == "invincible":
                    invincible = True
                    invincible_timer = INVINCIBLE_DURATION
                elif ability["type"] == "break":
                    break_blocks = True
                    break_timer = BREAK_DURATION
                abilities.remove(ability)

        # Draw everything
        screen.fill(SKY_COLOR)
        pygame.draw.rect(screen, OVERLAY_COLOR, overlay_rect, 500, border_radius=15)

        pygame.draw.rect(screen, BLUE, player, border_radius=8)
        for block in blocks:
            pygame.draw.rect(screen, BRICK_RED, block)
            pygame.draw.rect(screen, WHITE, block, 2)
        for ability in abilities:
            color = YELLOW if ability["type"] == "invincible" else GREEN
            pygame.draw.circle(screen, color, ability["rect"].center, 15)

        if invincible:
            pygame.draw.circle(screen, YELLOW, player.center, 30, 3) # ADD visual indicator for invincibility
        if break_blocks:
            pygame.draw.circle(screen, GREEN, player.center, 30, 3) # ADD visual indicator for break ability

        # Score display
        score_text = small_font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (20, 20))

    # ========================= SHOP SCREEN =========================
    elif game_state == 'shop':
        screen.fill("#a0ff6b")
        back_text = small_font.render("Press ESC to return", True, (0, 0, 0))
        screen.blit(back_text, (280, 280))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = 'menu'

    pygame.display.update()
    clock.tick(60)
