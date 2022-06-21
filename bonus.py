import pygame
import random

init_position = {
    "heal1" : (600,1300),
    "speed1" : (600, 1300),
    "teleport1" : (1300,1300)
}

class Bonus(pygame.sprite.Sprite):
    
    def __init__(self,type):
        super().__init__()
        self.init_x = random.randint(init_position[type][0],init_position[type][1])
        self.init_y = random.randint(init_position[type][0],init_position[type][1])
        self.position = [self.init_x, self.init_y]
        self.type = type

        self.sprite_sheet = pygame.image.load("assets/" + type + ".png")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

        self.taken = False
        self.respawn_tick = 0
        self.current_tick = 0

        images = {
            'heal1': (self.get_image(0, 0), self.get_image(0,16)),
            'speed1' : (self.get_image(0, 0), self.get_image(0,16))
        }
        self.images = images[type]
        self.image = images[type][0]
        self.image.set_colorkey ([0, 0, 0])
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

    def update(self):
        self.rect.topleft = self.position
        self.current_tick += 1
        if self.taken == True :
            self.image = self.images[1]
            self.image.set_colorkey ([0, 0, 0])
            if self.current_tick > 99 :
                self.respawn_tick += 1
            if self.respawn_tick == 40:
                self.taken = False
                self.respawn_tick = 0
                self.position = [random.randint(init_position[self.type][0], init_position[self.type][1]), random.randint(init_position[self.type][0], init_position[self.type][1])]
                self.image = self.images[0]
        if self.current_tick == 100:
            self.current_tick = 0
        if self.taken == False :
            self.animate()

    def animate(self):
        if self.current_tick % 20 == 0:
            self.position = [self.position[0], self.position[1] - 1]
        if self.current_tick % 40 == 0:
            self.position = [self.position[0], self.position[1] + 2]

    def get_image(self, x, y):
        image = pygame.Surface([16, 16])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 16))
        return image