import typing
import pygame
import abc


ContextType = typing.Any
StateType = typing.Any


class State(abc.ABC):
    _context: ContextType

    @property
    def context(self) -> ContextType:
        """The context property."""
        return self._context

    @context.setter
    def context(self, context: ContextType):
        self._context = context

    @abc.abstractmethod
    def update(self, events: list[pygame.event.Event]) -> None:
        ...

    @abc.abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        ...


class GrassyState(State):
    def __init__(self) -> None:
        super().__init__()
        self.font = pygame.font.Font(None, 32)
        self.surf = self.font.render("grassy", True, "green")

    def update(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._context.transition_to(RockyState())

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.surf, (50, 50))


class RockyState(State):
    def __init__(self) -> None:
        super().__init__()
        self.font = pygame.font.Font(None, 32)
        self.surf = self.font.render("rocky", True, "brown")

    def update(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._context.transition_to(GrassyState())

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.surf, (50, 50))


class Context:
    _state: StateType

    GAME_WORLD_SIZE = 450, 200

    def __init__(self, state: StateType) -> None:
        self.game_world_surface = pygame.Surface(self.GAME_WORLD_SIZE)
        self.transition_to(state)

    def transition_to(self, state: StateType) -> None:
        self._state = state
        self._state.context = self

    def update_state(self, events: list[pygame.event.Event]) -> None:
        self._state.update(events)

    def draw_state(self) -> None:
        self.game_world_surface.fill("grey")
        self._state.draw(self.game_world_surface)


