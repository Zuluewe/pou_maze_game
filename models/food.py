# model

from object import GameObject

class Food(GameObject):
    def __init__(self, position, sprite, score, sound):
        super().__init__(position, sprite)
        self.score = score
        self.sound = sound

    def on_collision(self):
        self.score += 1 # add one point
        self.sound.play()
        return super().on_collision()