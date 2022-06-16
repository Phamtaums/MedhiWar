import random
import pygame
import time

init_position={"ClubGoblin":(550,1300)}

class Ennemy(pygame.sprite.Sprite):

   def __init__(self,type, level):
       super().__init__()

       self.max_health = 3*(level//2+1)
       self.health = self.max_health
       self.damage = (level//2+1) * 2
       self.alive = True
       self.scored = False
       self.speed = 0.5
       self.random_move_tick = random.randint(1,80)
       self.current_tick = 0
       self.current_move = 0
       self.tick_revive = 0
       self.moving_to = False

       self.previous_attack_tick = 0
       self.attack_phase = 0
       self.attacking = False
       self.previous_attack_time = time.time()
       self.walking_phase = 0
       self.walking =  True
       self.previous_walking_tick = 0

       self.init_x = random.randint(init_position[type][0],init_position[type][1])
       self.init_y = random.randint(init_position[type][0],init_position[type][1])
       self.position = [self.init_x, self.init_y]
       self.type = type

       self.sprite_sheet = pygame.image.load(type+".png")
       self.image = self.get_image(0, 0)
       self.image.set_colorkey([0, 0, 0])
       self.rect = self.image.get_rect()

       self.images = {
           'down': (self.get_image(0, 0),self.get_image(16, 0), self.get_image(32, 0), self.get_image(48, 0), self.get_image(64, 0)),
           'left': (self.get_image(0, 48),self.get_image(16, 48), self.get_image(32, 48), self.get_image(48, 48), self.get_image(64, 48)),
           'right': (self.get_image(0, 32),self.get_image(16, 32), self.get_image(32, 32), self.get_image(48, 32), self.get_image(64, 32)),
           'up': (self.get_image(0, 16),self.get_image(16, 16), self.get_image(32, 16), self.get_image(48, 16), self.get_image(64, 16)),
           'attack_down': (self.get_image(0, 64),self.get_image(16,64),self.get_image(32,64)),
           'attack_up': (self.get_image(0, 80),self.get_image(16, 80),self.get_image(32, 80)),
           'attack_right': (self.get_image(0, 96),self.get_image(16, 96),self.get_image(32, 96)),
           'attack_left': (self.get_image(0, 112),self.get_image(16, 112),self.get_image(32, 112)),
           'dead' : self.get_image(48, 64)
       }

       self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
       self.old_position = self.position.copy()


   def save_location(self):
       self.old_position = self.position.copy()


   def change_animation(self, name):
       if self.attacking:
            self.image = self.images["attack_"+name][self.attack_phase]
            self.image.set_colorkey((0, 0, 0))
       elif self.walking :
            self.image = self.images[name][(self.walking_phase)]
            self.image.set_colorkey((0, 0, 0))
       else:
            self.image = self.images['dead']
            self.image.set_colorkey((0, 0, 0))

   def move_right(self):
       self.position[0] += self.speed
       self.change_animation('right')

   def move_left(self):
       self.position[0] -= self.speed
       self.change_animation('left')

   def move_up(self):
       self.position[1] -= self.speed
       self.change_animation('up')

   def move_down(self):
       self.position[1] += self.speed
       self.change_animation('down')

   def move_to(self, position):
       if self.position[0] <= position[0]:
           self.move_right()
       if self.position[1] <= position[1]:
           self.move_down()
       if self.position[0] >= position[0]:
           self.move_left()
       if self.position[1] >= position[1]:
           self.move_up()


   def update(self):
       self.rect.topleft = self.position
       self.feet.midbottom = self.rect.midbottom
       self.current_tick+=1
       self.move()
       if self.current_tick>100:
           self.current_tick=0

       if self.alive == False:
           if self.current_tick >99 :
               self.tick_revive +=1
               if self.tick_revive == 10:
                   self.tick_revive = 0
                   self.position = [random.randint(init_position[self.type][0],init_position[self.type][1]), random.randint(init_position[self.type][0],init_position[self.type][1])]
                   self.health = self.max_health
                   self.alive = True
                   self.walking = True
                   self.walking_phase = 0
                   self.scored = False
                   print('respawn')
       elif self.attack_phase <3 and self.attacking == True and self.current_tick%5 == 0:
           self.attack()
           self.attack_phase += 1
           if self.attack_phase == 3:
               self.attack_phase = 0

       elif self.walking and self.current_tick%10 == 0:
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

   def move(self):
       if not(self.moving_to):
           if self.current_tick == self.random_move_tick:
                self.current_move = random.choice(['right','down','up','left'])
           if self.current_move == 'right':
               self.move_right()
           elif self.current_move == 'up':
               self.move_up()
           elif self.current_move == 'left':
                self.move_left()
           elif self.current_move == 'down':
               self.move_down()

   def attack(self):
       self.change_animation(self.current_move)
       self.attacking = True

   def hurted(self, player_damage):
       if self.alive:
           self.health -= player_damage
           if self.health <= 0:
               self.alive = False
               self.walking = False


