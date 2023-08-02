import pygame

from src.menu import MainMenu

from src.agreements import *


class Game:
    def __init__(self):
        pygame.init()
        self._init_sound()
        pygame.font.init()
        self._init_screen()
        self._init_game_process()

    def _init_sound(self):
        pygame.mixer.init()
        self.music = pygame.mixer.Channel(0)
        self.sound = pygame.mixer.Channel(1)
        self.music.set_volume(MUSIC_LEVEL)
        self.sound.set_volume(SOUND_LEVEL)

    def _init_screen(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('406: The Game')
        self.start_screen = MainMenu(window=self)
        # TODO
        self.rules_screen = None
        self.settings_screen = None
        self.field_screen = None
        self.end_screen = None

        self.cur_screen = self.start_screen

    def _init_game_process(self):
        self.clock = pygame.time.Clock()
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            self.cur_screen.process_events()
            self.cur_screen.draw_screen()
            self.cur_screen.update()

            pygame.display.flip()

            self.clock.tick(FPS)

        self._exit()

    def _exit(self):
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.display.quit()
        pygame.quit()
