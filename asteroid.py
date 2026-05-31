import pygame
import random
from circleshape import CircleShape
from constants import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        # Draw a white circular wireframe representing the asteroid
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt: float) -> None:
        # Move the asteroid in a straight line relative to its velocity and time elapsed
        self.position += self.velocity * dt
    
    def split(self):
        # 1. Immediately kill the current asteroid
        self.kill()

        # 2. If it's a small asteroid, we are done
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # 3. Log the split event
        log_event("asteroid_split")

        # 4. Generate a random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)

        # 5. Create two new velocity vectors rotated by positive and negative angles
        vector1 = self.velocity.rotate(random_angle)
        vector2 = self.velocity.rotate(-random_angle)

        # 6. Compute the new smaller radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # 7. Spawn two new asteroids at the current position
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        # 8. Assign velocities and speed them up by multiplying by 1.2
        asteroid1.velocity = vector1 * 1.2
        asteroid2.velocity = vector2 * 1.2
