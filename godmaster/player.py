from __future__ import annotations
import abc
import pygame
from physics import PhysicalEntity, Side
import typing


class PlayerState(abc.ABC):
    _context: PlayerContext

    @property
    def context(self) -> PlayerContext:
        return self._context

    @context.setter
    def context(self, context: PlayerContext):
        self._context = context

class PlayerContext(PhysicalEntity):
    _state: PlayerState
    
    SPEED = pygame.Vector2(1.2, -3)
    MOVEMENT_MAP = {
        pygame.K_d: (SPEED.x, 0),
        pygame.K_a: (-SPEED.x, 0),
        pygame.K_w: (0, SPEED.y)
    }
    GRAVITY = 0.02

    def __init__(self, state: typing.Optional[PlayerState] = None)  -> None:
        super().__init__(
            mass = 3.4,
            acceleration=(0, self.GRAVITY),
            initial_velocity=(0, 0),
            position=(50, 0),
        )
        self.image = pygame.Surface((32, 32))
        self.image.fill("RED")
        self.rect = self.image.get_rect()
        self.set_collidable(True)
        self.touching_ground = False
        # self.transition_to(state)

    def transition_to(self, state: PlayerState) -> None:
        self._state = state
        self._state.context = self

    def collision_with_tile(self, proto_tile) -> None:
        if self.would_collide_with(proto_tile) == Side.BOTTOM:
            self.touching_ground = True
            self.velocity.y = 0
            self.acceleration.y = 0
        else:
            self.touching_ground = False

    def update(self, events: list[pygame.event.Event], keys, proto_tile) -> None:
        """Updates the player's movement.
        
        Args:
            events: A list of the events that occured between the last two event pumps.
            keys: The keys that were pressed between the last two get_pressed() calls.

        Returns:
            None
        """
        self.collision_with_tile(proto_tile)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if not event.key in self.MOVEMENT_MAP:
                    continue 
                
                if event.key == pygame.K_w and self.velocity.y < 0:
                    continue
                
                if event.key == pygame.K_w and self.acceleration.y == 0:
                    self.acceleration.y = self.GRAVITY

                speed = self.MOVEMENT_MAP[event.key]
                self.velocity.x += speed[0]
                self.velocity.y += speed[1]

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_d, pygame.K_a) and self.velocity.y == 0:
                    self.velocity.x = 0
        
        
        
        # if self.touching_ground and not any(key in (pygame.K_a, pygame.K_d) for key in keys) and self.velocity.x != 0:
            # self.velocity.x = 0
    
    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.position)

