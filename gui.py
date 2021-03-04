from time import sleep
import pygame

from constants import *


class GUI:
    def __init__(self, service, player):
        self.__service = service
        self.__player = player

    def drone_map_image(self, x, y, empty_color=WHITE, wall_color=BLACK, unknown=GRAY_BLUE):
        surface = self.__service.get_drone_map().get_surface()
        rows = self.__service.get_rows()
        columns = self.__service.get_columns()
        image = pygame.Surface((columns * COLUMN_LENGTH, rows * ROW_LENGTH))
        wall = pygame.Surface((COLUMN_LENGTH, ROW_LENGTH))
        empty = pygame.Surface((COLUMN_LENGTH, ROW_LENGTH))
        empty.fill(empty_color)
        wall.fill(wall_color)
        image.fill(unknown)
        for i in range(rows):
            for j in range(columns):
                if surface[i][j] == 1:
                    image.blit(wall, (j * COLUMN_LENGTH, i * ROW_LENGTH))
                elif surface[i][j] == 0:
                    image.blit(empty, (j * COLUMN_LENGTH, i * ROW_LENGTH))
        drona = pygame.image.load("drona.png")
        drona = pygame.transform.scale(drona, (COLUMN_LENGTH, ROW_LENGTH))
        if x is not None and y is not None:
            image.blit(drona, (y * COLUMN_LENGTH, x * ROW_LENGTH))
        return image

    def env_image(self, colour=BLUE, background=WHITE):
        rows = self.__service.get_rows()
        columns = self.__service.get_columns()
        surface = self.__service.get_env().get_surface()
        imagine = pygame.Surface((columns * COLUMN_LENGTH, rows * ROW_LENGTH))
        wall = pygame.Surface((COLUMN_LENGTH, ROW_LENGTH))
        wall.fill(colour)
        imagine.fill(background)
        for i in range(rows):
            for j in range(columns):
                if surface[i][j] == 1:
                    imagine.blit(wall, (j * COLUMN_LENGTH, i * ROW_LENGTH))
        return imagine

    def start(self):
        rows = self.__service.get_rows()
        columns = self.__service.get_columns()
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")
        screen = pygame.display.set_mode((columns * COLUMN_LENGTH * 2, rows * ROW_LENGTH))
        screen.fill(WHITE)
        screen.blit(self.env_image(), (0, 0))
        running = True
        has_quit = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    has_quit = True
                    running = False
                if self.__player == PLAY_BY_HAND and event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()
                    mapper = {pygame.K_UP: UP, pygame.K_DOWN: DOWN, pygame.K_LEFT: LEFT, pygame.K_RIGHT: RIGHT}#mapping the moves
                    for key in mapper.keys():
                        if pressed_keys[key]:
                            self.__service.move_by_user(mapper[key])
            if self.__player == MOVE_AUTOMATICALLY:
                running = running and self.__service.move_dfs()
                # pygame.event.post(event)
                pygame.event.pump()
                sleep(MOVE_WAIT)
            screen.blit(self.drone_map_image(self.__service.get_drone().x, self.__service.get_drone().y),
                        (columns * COLUMN_LENGTH, 0))
            pygame.display.flip()

        while not has_quit:
            can_quit = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    can_quit = True
            if can_quit:
                break
        pygame.quit()
