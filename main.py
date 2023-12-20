import pygame
import os
from models.player import Player
from models.attacks import Attacks
from models.proj import Proj
from models.button import Button
from models.text import Text
import time

FILE_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(FILE_DIR,"images", "EightBits.ttf")
WIDTH = 1280
HEIGHT = 840
FPS = 60

def start_game():
    global in_main_menu
    global player
    player.spawned = time.time()
    in_main_menu = False

def end_game():
    global run
    run = False

def resume():
    global pause
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

def draw_menu(screen, buttons, logo_text, button_font):

    logo_text.draw(screen)

    for button in buttons:
        button.draw(screen, button_font)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

in_main_menu = True
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
    Button("DIE AGAIN!!!",WIDTH/2, HEIGHT/2, 100, 50, (89, 89, 89), (255, 252, 252), restart),
    Button("Exit",WIDTH/2, HEIGHT/2 + 100, 100, 50, (89, 89, 89), (255, 252, 252), end_game)
]

selected_button = 0
main_menu_buttons[selected_button].is_selected = True
pause_menu_buttons[selected_button].is_selected = True
dead_menu_buttons[selected_button].is_selected = True

attacks = Attacks()

player_img = pygame.image.load(os.path.join(FILE_DIR, 'images','player.png'))
player = Player(WIDTH/2, HEIGHT/2, player_img, WIDTH, HEIGHT)


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

        logo_font = pygame.font.Font(FONT_DIR, 120)
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
                    dead = True
                    k = 0 #впадлу придумывать плавное затухане просто счетчиком ебанул

    pygame.display.flip()


pygame.quit()
