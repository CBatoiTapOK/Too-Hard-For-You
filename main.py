import pygame
import os
from models.player import Player
from models.attacks import Attacks
from models.proj import Proj
from models.button import Button
from models.text import Text
import time
# adaadad
FILE_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(FILE_DIR,"images", "EightBits.ttf")
FPS = 60

def start_game():
    global in_main_menu
    global player
    player.spawned = time.time()
    in_main_menu = False
    pygame.mixer.music.set_volume(0.15)

def end_game():
    global run
    run = False

def resume():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def restart():
    global projs
    global dead
    global player
    global attacks

    projs = []
    attacks.projs = []
    dead = False
    player_img = pygame.image.load(os.path.join(FILE_DIR, 'images','player.png'))
    player = Player(WIDTH/2, HEIGHT/2, player_img, WIDTH, HEIGHT)
    player.spawned = time.time()
    pygame.mixer.music.play(-1)

def handle_menu_events(event, buttons, selected_button):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            buttons[selected_button].is_selected = False
            selected_button = (selected_button - 1) % len(buttons)
            buttons[selected_button].is_selected = True
        elif event.key == pygame.K_DOWN:
            buttons[selected_button].is_selected = False
            selected_button = (selected_button + 1) % len(buttons)
            buttons[selected_button].is_selected = True
        elif event.key == pygame.K_RETURN:
            buttons[selected_button].action()
    return selected_button

pygame.init()
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
icon = pygame.image.load(os.path.join(FILE_DIR, "images" ,"icon.ico"))
pygame.display.set_icon(icon)
scr_inf = pygame.display.Info()
WIDTH = scr_inf.current_w
HEIGHT = scr_inf.current_h

clock = pygame.time.Clock()

in_main_menu = True
pygame.mixer.music.load(os.path.join(FILE_DIR, "music", "BG_music.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
main_menu_buttons = [
    Button("Start",WIDTH/2, HEIGHT/2, 100, 50, (89, 89, 89), (255, 252, 252), start_game),
    Button("Exit",WIDTH/2, HEIGHT/2 + 100, 100, 50, (89, 89, 89), (255, 252, 252), end_game)
]

pause = False
pause_menu_buttons = [
    Button("Resume",WIDTH/2, HEIGHT/2, 100, 50, (89, 89, 89), (255, 252, 252), resume),
    Button("Exit",WIDTH/2, HEIGHT/2 + 100, 100, 50, (89, 89, 89), (255, 252, 252), end_game)
]

dead = False
dead_menu_buttons = [
    Button("Restart",WIDTH/2, HEIGHT/2, 100, 50, (89, 89, 89), (255, 252, 252), restart),
    Button("Exit",WIDTH/2, HEIGHT/2 + 100, 100, 50, (89, 89, 89), (255, 252, 252), end_game)
]

selected_button = 0
main_menu_buttons[selected_button].is_selected = True
pause_menu_buttons[selected_button].is_selected = True
dead_menu_buttons[selected_button].is_selected = True

attacks = Attacks()

player_img = pygame.image.load(os.path.join(FILE_DIR, 'images','player.png'))
player = Player(WIDTH/2, HEIGHT/2, player_img, WIDTH, HEIGHT)
last_score_time = time.time()


run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if in_main_menu:
            selected_button = handle_menu_events(event, main_menu_buttons, selected_button)

        elif dead:
            selected_button = handle_menu_events(event, dead_menu_buttons, selected_button)

        elif pause:
            selected_button = handle_menu_events(event, pause_menu_buttons, selected_button)

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and (time.time() - player.spawned) >= 1.5:
                    pause = True
                    pygame.mixer.music.pause()
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.fill((0, 0, 0))
                    overlay.set_alpha(172)
                    screen.blit(overlay, (0, 0))

    if in_main_menu:
        screen.fill((0, 0, 0))

        logo_font = pygame.font.Font(FONT_DIR, 120)
        LOGO_TEXT = Text("Too Hard For You", WIDTH /2, 200, logo_font, (255, 255, 255))
        LOGO_TEXT.draw(screen)

        button_font = pygame.font.Font(FONT_DIR, 70)
        for button in main_menu_buttons:
                button.draw(screen, button_font)

    elif dead:
        if k <= (250 / 5):
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(5)
            screen.blit(overlay, (0, 0))
            k += 1

        score_font = pygame.font.Font(FONT_DIR, 120)
        SCORE_TEXT = Text(f"Score: {player.score}", WIDTH/2, (HEIGHT/2 - 160), score_font, (250, 250, 250))
        SCORE_TEXT.draw(screen)

        score_font = pygame.font.Font(FONT_DIR, 120)
        LOGO_TEXT = Text("Too Hard For You", WIDTH /2, 200, logo_font, (255, 255, 255))
        LOGO_TEXT.draw(screen)



        button_font = pygame.font.Font(FONT_DIR, 70)
        for button in dead_menu_buttons:
                button.draw(screen, button_font)


    elif pause:
        logo_font = pygame.font.Font(FONT_DIR, 120)
        LOGO_TEXT = Text("Too Hard For You", WIDTH /2, 200, logo_font, (255, 255, 255))
        LOGO_TEXT.draw(screen)

        button_font = pygame.font.Font(FONT_DIR, 70)
        for button in pause_menu_buttons:
            button.draw(screen, button_font)


    else:
        screen.fill((0, 0, 0))

        if not dead:
            if time.time() - last_score_time >= 1:
                player.score += 1
                last_score_time = time.time()
            score_font = pygame.font.Font(FONT_DIR, 120)
            SCORE_TEXT = Text(f"{player.score}", WIDTH/2, HEIGHT/2, score_font, (71, 71, 71))
            SCORE_TEXT.draw(screen)
            attacks.attack(player, (WIDTH, HEIGHT))
            attacks.attack(player, (WIDTH, HEIGHT))
            projs = attacks.projs
            player.move()
            player.update(screen)

        for proj in projs:
                proj.move()

                if not pause:
                    proj.render(screen)

                if proj in attacks.projs:
                    attacks.projs = proj.off_screen(attacks.projs, (WIDTH, HEIGHT))

                if not proj.rotated:
                    proj.img = pygame.transform.rotate(pygame.transform.scale(Proj.obstacles[proj.obs_type], proj.img_size), proj.rotation)
                    proj.rotated = True

                if proj.rect.colliderect(player.rect) and (time.time() - player.spawned >= 1.5):
                    pygame.mixer.music.stop()
                    dead = True
                    k = 0 #впадлу придумывать плавное затухане просто счетчиком сделал

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
