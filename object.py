from abc import ABC, abstractmethod
import pygame

class GameObject(ABC):
    def __init__(self, position, sprite = None):
        self.position = position
        self.rect = self.sprite.get_rect(topleft=position)
        self.active = True
    
    @property
    def draw(self, screen):
        if self.active:
            screen.blit(self.sprite, self.rect)

    def check_collision(self, player_rect):
        if self.active and self.rect.colliderect(player_rect):
            self.on_collision()
            self.active = False
    
    @abstractmethod
    def on_collision(self):
        pass
    
