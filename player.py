import pygame
import time
class Player(pygame.sprite.Sprite):

   def __init__(self, x, y):
       super().__init__()
       self.sprite_sheet = pygame.image.load("assets/player.png")
       self.image = self.get_image(0, 0)
       self.image.set_colorkey ([0, 0, 0])
       self.rect = self.image.get_rect()
       self.position = [x, y]
       self.images = {
           'down': (self.get_image(0, 0),self.get_image(16, 0),self.get_image(32, 0),self.get_image(48, 0),self.get_image(64, 0)),
           'left': (self.get_image(0, 48),self.get_image(16, 48),self.get_image(32, 48),self.get_image(48, 48),self.get_image(64, 48)),
           'right': (self.get_image(0, 32),self.get_image(16, 32),self.get_image(32, 32),self.get_image(48, 32),self.get_image(64, 32)),
           'up': (self.get_image(0, 16),self.get_image(16, 16),self.get_image(32, 16),self.get_image(48, 16),self.get_image(64, 16)),
           'attack_down': (self.get_image(0, 64),self.get_image(16,64),self.get_image(32,64),self.get_image(48,64),self.get_image(64,64)),
           'attack_up': (self.get_image(0, 80),self.get_image(16, 80),self.get_image(32, 80),self.get_image(48, 80),self.get_image(64, 80)),
           'attack_right': (self.get_image(0, 96),self.get_image(16, 96),self.get_image(32, 96),self.get_image(48, 96),self.get_image(64, 96)),
           'attack_left': (self.get_image(0, 112),self.get_image(16, 112),self.get_image(32, 112),self.get_image(48, 112),self.get_image(64, 112))
       }
       self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)         # pied du joueur
       self.old_position = self.position.copy()

       self.current_tick = 0
       self.speed = 4
       self.xp = 0
       self.max_health = 10*((1+self.xp)//2+1)
       self.health = self.max_health
       self.damage = 3*self.xp+3

       self.score_value = 0

       self.previous_attack_tick = 0
       self.attack_phase = 0
       self.attacking = False
       self.previous_attack_time = time.time()

       self.walking_phase = 0
       self.walking =  False
       self.previous_walking_tick = 0
       self.current_move = 'down'

   def save_location(self): self.old_position = self.position.copy()

   def change_animation(self, name):
       if self.attacking:
            self.image = self.images["attack_"+name][self.attack_phase]
            self.image.set_colorkey((0, 0, 0))
       else :
            self.image = self.images[name][(self.walking_phase)]
            self.image.set_colorkey((0, 0, 0))


   def move_right(self):
       self.current_move = 'right'
       self.position[0] += self.speed
       if not self.attacking:
            self.change_animation('right')

   def move_left(self):
       self.current_move = 'left'
       self.position[0] -= self.speed
       if not self.attacking:
           self.change_animation('left')

   def move_up(self):
       self.current_move = 'up'
       self.position[1] -= self.speed
       if not self.attacking:
            self.change_animation('up')

   def move_down(self):
       self.current_move = 'down'
       self.position[1] += self.speed
       if not self.attacking:
            self.change_animation('down')

   def update(self):
       self.current_tick +=1
       self.rect.topleft = self.position
       self.feet.midbottom = self.rect.midbottom
       if self.current_tick == 100:
           self.current_tick = 0
       if self.attack_phase <4 and self.attacking == True and self.current_tick%5 == 0:
           self.attack()
           self.attack_phase += 1
       if self.walking == True and self.current_tick%5 == 0:
           self.walking_phase += 1
           if self.walking_phase == 4:
               self.walking_phase = 0
               self.previous_walking_tick = self.current_tick


   def move_back(self):
       self.position = self.old_position
       self.rect.topleft = self.position
       self.feet.midbottom = self.rect.midbottom

   def get_image(self, x, y):
        image = pygame.Surface([16, 16])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 16))
        return image

   def attack(self):
       self.change_animation(self.current_move)

   def hurted(self, damage):
       self.health -= damage

   def add_score(self, amount):
       self.score_value += amount

   def heal(self,amount):
       self.health += amount
       if self.health > self.max_health:
           self.health = self.max_health


