import pygame
from os import path
from src.agreements import *
from src.base_screen import BaseScreen


# Class for main menu screen
class MainMenu(BaseScreen):
    def __init__(self, window=None):
        self.window = window
        self._init_image()
        self._init_text()
        self._init_logic()

    def start_music(self):
        self.window.music.stop()
        self.window.music.play(pygame.mixer.Sound(
            path.join(DATA_PATH, SOUND_PATH, 'start_screen.wav')), loops=-1)
        self.window.music.set_volume(SOUND_LEVEL)

    def _init_image(self):
        self.background_image = pygame.image.load(
            path.join(DATA_PATH, IMAGE_PATH, BACKGROUND_PATH, 'cybercity.jpg'))
        self.background_image = pygame.transform.scale(self.background_image,
                                                       WINDOW_SIZE)
        self.fading_image = pygame.image.load(
            path.join(DATA_PATH, IMAGE_PATH, BACKGROUND_PATH, 'fading.png'))
        self.fading_image = pygame.transform.scale(self.fading_image,
                                                   WINDOW_SIZE)

    def _init_text(self):
        self.TITLE_MIN_Y = int(WINDOW_SIZE[1] / 36)
        self.TITLE_MAX_Y = int(WINDOW_SIZE[1] / 15)
        self.TEXT_X = WINDOW_SIZE[0] / 48
        self.START_Y = int(WINDOW_SIZE[0] / 6)
        self.Y_PADDING = int(WINDOW_SIZE[0] / 12)
        self.TITLE_BASIC_SPEED = 0.01
        self.TITLE_SPEED_MULTIPLIER = 1.01
        self.TITLE_FONT_SIZE = int(WINDOW_SIZE[0] / 12)
        self.SUBTITLE_FONT_SIZE = int(WINDOW_SIZE[0] / 24)
        self.intro_text = ['406: The Game',
                           'START',
                           'SETTINGS',
                           'EXIT']
        self.title_font = pygame.font.Font(
            pygame.font.match_font('lucidasans'), self.TITLE_FONT_SIZE)
        self.title_y = self.TITLE_MIN_Y
        self.title_speed = self.TITLE_BASIC_SPEED
        self.subtitle_font = pygame.font.Font(
            pygame.font.match_font('lucidaconsole'), self.SUBTITLE_FONT_SIZE)

    def _init_logic(self):
        self.selected = 0
        self.press_tick = 0
        self.PRESS_DELAY = 75

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False

        keys = pygame.key.get_pressed()
        tick = pygame.time.get_ticks()

        if tick - self.press_tick >= self.PRESS_DELAY:
            if keys[pygame.K_UP]:
                self.selected -= 1
                self.selected %= 3
                print(f'UP {self.selected}')
            if keys[pygame.K_DOWN]:
                self.selected += 1
                self.selected %= 3
                print(f'DOWN {self.selected}')
            if keys[pygame.K_RETURN]:
                if self.selected == 0:
                    self.window.cur_screen = self.window.field_screen
                elif self.selected == 1:
                    self.window.cur_screen = self.window.settings_screen
                else:
                    self.window.running = False
            self.press_tick = pygame.time.get_ticks()

    # Draws screen
    def draw_screen(self):
        self._draw_image()
        self._draw_text()
        self._draw_fading()
        self._move_title()

    # Draws background
    def _draw_image(self):
        self.window.screen.blit(self.background_image, (0, 0))

    # Draws text and moves title
    def _draw_text(self):
        string_title = self.title_font.render(
            self.intro_text[0], True, pygame.Color('white')
        )
        string_start = self.subtitle_font.render(
            self.intro_text[1], True, pygame.Color(
                'yellow' if self.selected == 0 else 'white')
        )
        string_settings = self.subtitle_font.render(
            self.intro_text[2], True, pygame.Color(
                'yellow' if self.selected == 1 else 'white')
        )
        string_exit = self.subtitle_font.render(
            self.intro_text[3], True, pygame.Color(
                'yellow' if self.selected == 2 else 'white')
        )
        rect_title = string_title.get_rect()
        rect_start = string_start.get_rect()
        rect_settings = string_settings.get_rect()
        rect_exit = string_exit.get_rect()
        rect_title = rect_title.move(self.TEXT_X, self.title_y)
        rect_start = rect_start.move(self.TEXT_X, self.START_Y)
        rect_settings = rect_settings.move(self.TEXT_X,
                                           self.START_Y + self.Y_PADDING)
        rect_exit = rect_exit.move(self.TEXT_X,
                                   self.START_Y + self.Y_PADDING * 2)
        self.window.screen.blit(string_title, rect_title)
        self.window.screen.blit(string_start, rect_start)
        self.window.screen.blit(string_settings, rect_settings)
        self.window.screen.blit(string_exit, rect_exit)

    # Moves title
    def _move_title(self):
        if self.TITLE_MIN_Y <= self.title_y <= self.TITLE_MAX_Y:
            self.title_speed *= self.TITLE_SPEED_MULTIPLIER
            self.title_y += self.title_speed
        elif self.title_y < self.TITLE_MIN_Y:
            self.title_speed = self.TITLE_BASIC_SPEED
            self.title_y = self.TITLE_MIN_Y
        else:
            self.title_speed = -self.TITLE_BASIC_SPEED
            self.title_y = self.TITLE_MAX_Y

    # Draws fading
    def _draw_fading(self):
        if self.fading_image.get_alpha() != 0:
            self.fading_image.set_alpha(self.fading_image.get_alpha() - 1)
        self.window.screen.blit(self.fading_image, (0, 0))
