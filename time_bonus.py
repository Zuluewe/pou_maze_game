from object import GameObject

class TimeBonus(GameObject):
    def __init__(self, position, sprite, timer, sound):
        super().__init__(position, sprite)
        self.timer = timer
        self.sound = sound

    def on_collision(self):
        self.timer += 5 # add 5 second to time
        self.sound.play()
        return super().on_collision()