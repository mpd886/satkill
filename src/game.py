import os
import math
import sys
import random
import pygame

class Satellite:
    def __init__(self, imgfile, dx):
        self.dx = dx
        self.img = pygame.image.load(imgfile)
        self.theta = 0
        self.x = 100 
        self.y = 100

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.img.get_rect().width, self.img.get_rect().height)

    def update(self, elapsed, bounds):
        self.theta = (self.theta + (elapsed*self.dx)) % 360
        rads = math.radians(self.theta)
        self.x += elapsed*self.dx
        self.y += math.sin(rads)
        if self.x > bounds.width:
            self.x = -64
        return False
    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

class Missle:
    def __init__(self, imgfile, x, y, dy):
        self.x = x
        self.y = y
        self.dy = dy
        self.img = pygame.image.load(imgfile)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.img.get_rect().width, self.img.get_rect().height)

    def update(self, elapsed, bounds):
        self.y += elapsed * self.dy
        if self.y < -self.img.get_rect().height:
            return True
        return False

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))


class Explosion:
    def __init__(self, x, y):
        self.particles = []
        self.timeAlive = 3000
        for d in range(100):
            self.particles.append(Particle(x, y, random.randint(0, 360)))

    def get_rect(self):
        return pygame.Rect(-10, -10, 0, 0)

    def update(self, elapsed, bounds):
        self.timeAlive -= elapsed
        for p in self.particles:
            p.update(elapsed)
        if self.timeAlive <= 0:
            return True
        else:
            return False

    def draw(self, surface):
        for p in self.particles:
            surface.fill(p.color, pygame.Rect(p.x, p.y, 10, 10))


class Particle:
    def __init__(self, x, y, theta):
        self.color = random.choice([(255, 0,0), (255, 165, 0), (255, 215, 0), (255, 140, 0), (255, 99, 71)])
        self.x = x
        self.y = y
        self.rads = math.radians(theta)
        self.dx = random.random() * math.cos(self.rads) 
        self.dy = random.random() * math.sin(self.rads)
        self.velocity = random.random()

    def update(self, elapsed):
        self.x += elapsed*self.dx
        self.y += elapsed*self.dy


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.display_list = [Satellite("satellite.png", 0.3)]

    def draw(self):
        self.screen.fill((0,0,0))
        for obj in self.display_list:
            obj.draw(self.screen)
        pygame.display.flip()

    def collision(self, obj):
        for other in self.display_list:
            if other != obj and obj.get_rect().colliderect(other.get_rect()):
                return other        
        return None

    def update(self):
        elapsed = self.clock.tick(40)
        for obj in self.display_list:
            if obj.update(elapsed, self.screen.get_rect()):
                self.display_list.remove(obj)
            else:
                collided = self.collision(obj)
                if collided is not None:
                    self.display_list.append(Explosion(obj.x, obj.y))
                    self.display_list.remove(collided)
                    self.display_list.remove(obj)
                    self.display_list.append(Satellite("satellite.png", 0.3))

    def gameloop(self):
        while True:
            self.draw()
            self.update()
            self.check_input()

    def check_input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    sys.exit(0)
                if e.key == pygame.K_SPACE:
                    self.display_list.append(Missle("missle.png", 400, self.screen.get_rect().height + 100, -0.8))

if __name__ == "__main__":
   pygame.init()
   Game().gameloop()

