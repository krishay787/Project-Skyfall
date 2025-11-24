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



cloud_surf = pygame.image.load('Graphics/cloud.png').convert_alpha()
cloud_surf = pygame.transform.scale(cloud_surf, (155, 93))
cloud_rect = cloud_surf.get_rect(center=(260, 160))
cloud_rect_2 = cloud_surf.get_rect(center=(550, 120))

cloud_surf_2 = pygame.transform.scale(cloud_surf, (126, 76))
cloud_rect_3 = cloud_surf_2.get_rect(topleft=(120, 448))
cloud_rect_4 = cloud_surf_2.get_rect(topleft=(545, 480))

overlay_shape = pygame.surface.Surface((774, 568))
overlay_rect = overlay_shape.get_rect(center=(400, 300))

play_btn = pygame.image.load('Graphics/playbutton.png').convert_alpha()
play_btn_rect = play_btn.get_rect(topleft=(185, 260))

credits_btn = pygame.image.load('Graphics/credits.png').convert_alpha()
credits_btn_rect = credits_btn.get_rect(topleft=(438, 260))

highscore_panel = pygame.image.load('Graphics/highscorepanel.png').convert_alpha()
highscore_panel_rect = highscore_panel.get_rect(topleft=(193, 358))

mapchooser = pygame.image.load('Graphics/map_panel.png').convert_alpha()
mapchooser_rect = mapchooser.get_rect(center=(400, 300))

classic_btn = pygame.image.load('Graphics/classic_btn.png').convert_alpha()
classic_btn_rect = classic_btn.get_rect(center=(220, 260))

space_btn = pygame.image.load('Graphics/space_btn_.png').convert_alpha()
space_btn_rect = space_btn.get_rect(center=(400, 260))

storm_btn = pygame.image.load('Graphics/storm_btn.png').convert_alpha()
storm_btn_rect = storm_btn.get_rect(center=(580, 260))

ship_surf = pygame.image.load('Graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center=(400, 520))

anchor_surf = pygame.image.load('Graphics/_anchor.png').convert_alpha()
anchor_rect = anchor_surf.get_rect(center=(400, 520))

spaceship_surf = pygame.image.load('Graphics/spaceship.png').convert_alpha()
spaceship_rect = spaceship_surf.get_rect(center=(400, 520))

meteor_surf = pygame.image.load('Graphics/meteor.png').convert_alpha()
meteor_rect = meteor_surf.get_rect(center=(400, 520))

border_surf = pygame.image.load('Graphics/_border.png').convert_alpha()
border_rect = border_surf.get_rect(topleft=(0, 0))


pygame.mixer.init()
music_classic = 'Audio\playing_music.mp3'
music_space = 'Audio\space_music.mp3'
music_storm = 'Audio\storm_music.mp3'
music_playing = False


# Gameplay variables
player = pygame.Rect(400 - 25, 520, 50, 50)
ship_surf = pygame.transform.scale(ship_surf, (50, 50))
spaceship_surf = pygame.transform.scale(spaceship_surf, (50, 50))
player_speed = 7
blocks = []
block_speed = 6
anchor_surf = pygame.transform.scale(anchor_surf, (80, 80))
meteor_surf = pygame.transform.scale(meteor_surf, (60, 60))
abilities = []
ability_speed = 10


spawn_timer = 0
invincible = False
break_blocks = False
invincible_timer = 0
break_timer = 0
INVINCIBLE_DURATION = 300
BREAK_DURATION = 180
score = 0
spawn_delay = 40
min_spawn_delay = 10

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
    rect = pygame.Rect(x, -30, 60, 30)
    blocks.append({"rect": rect, "image": None})
    

def spawn_ability():
    x = random.randint(0, 770)
    ability_type = random.choice(["invincible", "break"])
    abilities.append({"rect": pygame.Rect(x, -30, 30, 30), "type": ability_type})

def update_block_speed(score):
    base_speed = 6
    max_speed = 50
    increment = score // 500
    return min(base_speed + increment, max_speed)

def load_highscores():
    try:
        with open("highscores.txt", "r") as f:
            scores = [int(line.strip()) for line in f.readlines()]
            return sorted(scores, reverse=True)[:5]
    except:
        return [0, 0, 0, 0, 0]

def save_highscores(highscores):
    with open("highscores.txt", "w") as f:
        for s in highscores:
            f.write(str(s) + "\n")

highscores = load_highscores()


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
        screen.blit(credits_btn, credits_btn_rect)
        screen.blit(highscore_panel, highscore_panel_rect)
        for i, hs in enumerate(highscores):
            hs_text = small_font.render(f"{i+1}. {hs}", True, ('#FFFFFF'))
            screen.blit(hs_text, (280, 410 + i * 30))

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
                elif credits_btn_rect.collidepoint(event.pos):
                    game_state = 'credits'


    

    # ========================= GAMEPLAY ============================
    elif game_state == 'choosing':
        screen.blit(mapchooser, mapchooser_rect)
        screen.blit(classic_btn, classic_btn_rect)
        screen.blit(space_btn, space_btn_rect)
        screen.blit(storm_btn, storm_btn_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if classic_btn_rect.collidepoint(event.pos):
                    reset_game()
                    pygame.mixer.music.load(music_classic)
                    music_playing = False
                    game_state = 'playing1'
                elif space_btn_rect.collidepoint(event.pos):
                    reset_game()
                    pygame.mixer.music.load(music_space)
                    music_playing = False
                    game_state = 'playing2'  # Placeholder for space mode
                elif storm_btn_rect.collidepoint(event.pos):
                    reset_game()
                    pygame.mixer.music.load(music_storm)
                    music_playing = False
                    current_skin = ship_surf  # Reset to default skin for storm mode
                    game_state = 'playing3'  # Placeholder for storm mode

    elif game_state == 'game_over':
        pygame.mixer.music.stop()
        music_playing = False

        screen.blit(game_over_text, game_over_rect)
        screen.blit(main_menu_text, main_menu_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_state = 'menu'

    

    elif game_state == 'playing1':

        if not music_playing:
            pygame.mixer.music.play(-1) 
            music_playing = True

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

        spawn_delay = max(min_spawn_delay, 40 - (score // 100))
        if spawn_timer % spawn_delay == 0:
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
            block["rect"].y += block_speed
            if block["rect"].top > 600:
                blocks.remove(block)
            elif block["rect"].colliderect(player):
                if break_blocks:
                    blocks.remove(block)
                elif not invincible:
                    game_state = 'game_over'
                    highscores.append(score)
                    highscores = sorted(highscores, reverse=True)[:5]
                    save_highscores(highscores) # ADD GAME OVER LOGIC HERE

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
            pygame.draw.rect(screen, BRICK_RED, block["rect"])
            pygame.draw.rect(screen, WHITE, block["rect"], 2)
        for ability in abilities:
            color = YELLOW if ability["type"] == "invincible" else GREEN
            pygame.draw.circle(screen, color, ability["rect"].center, 15)

        if invincible:
            pygame.draw.circle(screen, YELLOW, player.center, 30, 3) # ADD visual indicator for invincibility
        if break_blocks:
            pygame.draw.circle(screen, GREEN, player.center, 30, 3) # ADD visual indicator for break ability

        screen.blit(border_surf, border_rect)

        # Score display
        score_text = small_font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (50, 20))

    elif game_state == 'playing2':

        current_skin = spaceship_surf

        for block in blocks:
            block["image"] = meteor_surf

        if not music_playing:
            pygame.mixer.music.play(-1) 
            music_playing = True

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

        spawn_delay = max(min_spawn_delay, 40 - (score // 100))
        if spawn_timer % spawn_delay == 0:
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
            block["rect"].y += block_speed
            if block["rect"].top > 600:
                blocks.remove(block)
            elif block["rect"].colliderect(player):
                if break_blocks:
                    blocks.remove(block)
                elif not invincible:
                    game_state = 'game_over'
                    highscores.append(score)
                    highscores = sorted(highscores, reverse=True)[:5]
                    save_highscores(highscores) # ADD GAME OVER LOGIC HERE

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
        pygame.draw.rect(screen, '#000000', overlay_rect, 500, border_radius=15)
        screen.blit(border_surf, border_rect)

        screen.blit(current_skin, player)
        for block in blocks:
            if block["image"] is None:
                pygame.draw.rect(screen, BRICK_RED, block["rect"])
                pygame.draw.rect(screen, WHITE, block["rect"], 2)
            else:
                screen.blit(block["image"], block["rect"])
        for ability in abilities:
            color = YELLOW if ability["type"] == "invincible" else GREEN
            pygame.draw.circle(screen, color, ability["rect"].center, 15)

        if invincible:
            pygame.draw.circle(screen, YELLOW, player.center, 30, 3) # ADD visual indicator for invincibility
        if break_blocks:
            pygame.draw.circle(screen, GREEN, player.center, 30, 3) # ADD visual indicator for break ability

        screen.blit(border_surf, border_rect)

        # Score display
        score_text = small_font.render(f"Score: {score}", True, ('#FFFFFF'))
        screen.blit(score_text, (50, 20))

    elif game_state == 'playing3':

        current_skin = ship_surf

        for block in blocks:
            block["image"] = anchor_surf

        if not music_playing:
            pygame.mixer.music.play(-1) 
            music_playing = True

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

        spawn_delay = max(min_spawn_delay, 40 - (score // 100))
        if spawn_timer % spawn_delay == 0:
            spawn_block()
            blocks[-1]["image"] = anchor_surf
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
            block["rect"].y += block_speed
            if block["rect"].top > 600:
                blocks.remove(block)
            elif block["rect"].colliderect(player):
                if break_blocks:
                    blocks.remove(block)
                elif not invincible:
                    game_state = 'game_over'
                    highscores.append(score)
                    highscores = sorted(highscores, reverse=True)[:5]
                    save_highscores(highscores) # ADD GAME OVER LOGIC HERE

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
        pygame.draw.rect(screen, "#97B2DC", overlay_rect, 500, border_radius=15)
        screen.blit(border_surf, border_rect)

        screen.blit(current_skin, player)
        for block in blocks:
            if block["image"] is None:
                pygame.draw.rect(screen, BRICK_RED, block["rect"])
                pygame.draw.rect(screen, WHITE, block["rect"], 2)
            else:
                screen.blit(block["image"], block["rect"])
        for ability in abilities:
            color = YELLOW if ability["type"] == "invincible" else GREEN
            pygame.draw.circle(screen, color, ability["rect"].center, 15)

        if invincible:
            pygame.draw.circle(screen, YELLOW, player.center, 30, 3) # ADD visual indicator for invincibility
        if break_blocks:
            pygame.draw.circle(screen, GREEN, player.center, 30, 3) # ADD visual indicator for break ability

        screen.blit(border_surf, border_rect)

        # Score display
        score_text = small_font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (50, 20))

    # ========================= CREDITS SCREEN =========================
    elif game_state == 'credits':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(SKY_COLOR)
        pygame.draw.rect(screen, "#80e8ff", overlay_rect, 500, border_radius=15)
        back_text = small_font.render("Press ESC to return", True, ('#000000'))
        
        text1 = screen.blit(small_font.render("Krishay Kanchan", True, ("#000000")), (250, 50))
        text2 = screen.blit(small_font.render("Bhargav Taware", True, ('#000000')), (250, 120))
        text3 = screen.blit(small_font.render("Zaid Maniar", True, ('#000000')), (250, 190))
        text4 = screen.blit(small_font.render("Varun Khanchandani", True, ('#000000')), (250, 250))
        text5 = screen.blit(small_font.render("Priyanshu Pathak", True, ('#000000')), (250, 320))
        text6 = screen.blit(small_font.render("Sean Sebastian", True, ('#000000')), (250, 390))
        text7 = screen.blit(small_font.render("Yohan Billimoria", True, ('#000000')), (250, 460))
        screen.blit(back_text, (30, 20))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = 'menu'

    pygame.display.update()
    clock.tick(60)
