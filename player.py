import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen: pygame.Surface):
        # Draw the player as a white polygon outline using the triangle points
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
    
    def rotate(self, dt: float):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt: float):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    
    def shoot(self):
        # If the cooldown timer is greater than 0, block the shot
        if self.cooldown_timer > 0:
            return
        # Otherwise, reset the timer and spawn the shot
        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        # Create a new shot at the player's current position
        new_shot = Shot(self.position.x, self.position.y)
        
        # Start with a vector pointing "up" (0, 1)
        velocity_vector = pygame.Vector2(0, 1)
        
        # Rotate it to match the player's rotation angle
        velocity_vector = velocity_vector.rotate(self.rotation)
        
        # Scale it up by the shooting speed constant
        new_shot.velocity = velocity_vector * PLAYER_SHOOT_SPEED
      
    def update(self, dt: float) -> None:
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            # Rotate left by reversing the delta time
            self.rotate(-dt)
        if keys[pygame.K_d]:
            # Rotate right normally
            self.rotate(dt)
        if keys[pygame.K_w]:
            # Move forward
            self.move(dt)
        if keys[pygame.K_s]:
            # Move backward by reversing delta time
            self.move(-dt)
        if keys[pygame.K_SPACE]:  # <-- Check for spacebar
            self.shoot()
