from physics import PhysicalEntity, pygame
from .common import GAME_WORLD_WIDTH, GAME_WORLD_HEIGHT


class PrototypeTile(PhysicalEntity):
    def __init__(self) -> None: 

        super().__init__(
            mass=0.0,
            acceleration=(0, 0),
            initial_velocity=(0.0, 0.0),
            position=(0, GAME_WORLD_HEIGHT - 20),
        )
        self.image = pygame.Surface((GAME_WORLD_WIDTH, 20))
        self.image.fill("purple")
        self.rect = self.image.get_rect()
        self.set_collidable(True)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.position)
    

