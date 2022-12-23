from __future__ import annotations

import pygame
import abc

from godmaster.common import GAME_WORLD_WIDTH, GAME_WORLD_HEIGHT # type: ignore
from physics import World2D 
from godmaster.player import PlayerContext  # type: ignore
from godmaster.tiles import PrototypeTile # type: ignore



class GameWorldState(abc.ABC):
    _context: GameWorldContext
    player: PlayerContext
    proto_tile: PrototypeTile

    @property
    def context(self) -> GameWorldContext:
        """The context property."""
        return self._context

    @context.setter
    def context(self, context: GameWorldContext):
        self._context = context

    @abc.abstractmethod
    def update(self, events: list[pygame.event.Event], keys) -> None:
        ...

    @abc.abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        ...


class NormalState(GameWorldState):
    def __init__(self) -> None:
        super().__init__()
        self.player = PlayerContext()
        self.proto_tile = PrototypeTile()

    def update(self, events: list[pygame.event.Event], keys) -> None:

        self.player.update(events, keys, self.proto_tile)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                self._context.transition_to(RockyState())

    def draw(self, screen: pygame.surface.Surface) -> None:
        self.player.draw(screen)
        self.proto_tile.draw(screen)

class RockyState(GameWorldState):
    def __init__(self) -> None:
        super().__init__()
        self.font = pygame.font.Font(None, 32)
        self.surf = self.font.render("rocky", True, "brown")

    def update(self, events: list[pygame.event.Event], keys) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._context.transition_to(NormalState())

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.surf, (50, 50))


class GameWorldContext:
    _state: GameWorldState 


    def __init__(self, state: GameWorldState) -> None:
        self.world = World2D()
        self.game_world_surface = pygame.Surface((GAME_WORLD_WIDTH, GAME_WORLD_HEIGHT))
        self.game_world_rect = self.game_world_surface.get_rect()
        self.transition_to(state)

        self.world.add(self._state.player)
        self.world.add(self._state.proto_tile)


    def transition_to(self, state: GameWorldState) -> None:
        self._state = state
        self._state.context = self

    def update_state(self, events: list[pygame.event.Event], keys) -> None:
        self.world.update()
        
        self._state.update(events, keys)

    def draw_state(self, screen: pygame.surface.Surface) -> None:
        self.game_world_surface.fill("grey")
        self._state.draw(self.game_world_surface)
        screen.blit(self.game_world_surface, self.game_world_rect) 
