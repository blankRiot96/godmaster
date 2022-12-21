import pygame
from .game_world.world import Context, GrassyState
from .common import SCREEN_WIDTH, SCREEN_HEIGHT, FPS_CAP


def handle_quit(events: list[pygame.event.Event]) -> None:
    for event in events:
        if event.type == pygame.QUIT:
            raise SystemExit


def game_loop(screen: pygame.surface.Surface, clock: pygame.time.Clock, context: Context):
    events = pygame.event.get()
    handle_quit(events)
    context.update_state(events)
    
    screen.fill("black")
    context.draw_state()
    screen.blit(context.game_world_surface, (10, 10))

    pygame.display.flip()
    clock.tick(FPS_CAP)


def game():
    pygame.init()

    # We want a resizable window since we will manually be handling the scaling
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    context = Context(GrassyState())

    while True:
        game_loop(screen, clock, context)
