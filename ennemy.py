import random
import pygame
import time

init_position={"ClubGoblin": (600, 1300), "Slime1": (600, 1300), "Yeti": (600, 1300), 'SpearGoblin': (600, 1300)}
speed = {"ClubGoblin": (0.5, 1), "Slime1": (0.2, 0.2), "Yeti": (0.3, 0.7), "SpearGoblin": (0.5, 1)}
score_given = {"ClubGoblin": 3, "Slime1": 1, "Yeti": 5, "SpearGoblin": 3}
health = {"ClubGoblin": 5, "Slime1": 3, "Yeti": 7, "SpearGoblin": 5}
knockback = {"ClubGoblin": 10, "Slime1": 40, "Yeti": 6, 'SpearGoblin': 10}
damage = {"ClubGoblin": 2, "Slime1": 1, "Yeti": 4, "SpearGoblin": 3}
attack_speed = {"ClubGoblin": 2, "Slime1": 1, "Yeti": 3, "SpearGoblin": 2}

class Ennemy(pygame.sprite.Sprite):

   def __init__(self,type):
       super().__init__()

       self.score_given = score_given[type]
       self.max_health = health[type]
       self.health = self.max_health
       self.damage = damage[type]
       self.alive = True
       self.scored = False
       self.speeds = speed[type]
       self.walking_speed = speed[type][0]

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
       self.walking = True
       self.previous_walking_tick = 0
       self.attack_speed = attack_speed[type]

       self.init_x = random.randint(init_position[type][0],init_position[type][1])
       self.init_y = random.randint(init_position[type][0],init_position[type][1])
       self.position = [self.init_x, self.init_y]
       self.type = type

       self.sprite_sheet = pygame.image.load("assets/"+type+".png")
       self.image = self.get_image(0, 0)
       self.image.set_colorkey([0, 0, 0])
       self.rect = self.image.get_rect()

       images = {
    "ClubGoblin" : {
           'down': (self.get_image(0, 0),self.get_image(16, 0), self.get_image(32, 0), self.get_image(48, 0), self.get_image(64, 0)),
           'left': (self.get_image(0, 48),self.get_image(16, 48), self.get_image(32, 48), self.get_image(48, 48), self.get_image(64, 48)),
           'right': (self.get_image(0, 32),self.get_image(16, 32), self.get_image(32, 32), self.get_image(48, 32), self.get_image(64, 32)),
           'up': (self.get_image(0, 16),self.get_image(16, 16), self.get_image(32, 16), self.get_image(48, 16), self.get_image(64, 16)),
           'attack_down': (self.get_image(0, 64),self.get_image(16,64),self.get_image(32,64)),
           'attack_up': (self.get_image(0, 80),self.get_image(16, 80),self.get_image(32, 80)),
           'attack_right': (self.get_image(0, 96),self.get_image(16, 96),self.get_image(32, 96)),
           'attack_left': (self.get_image(0, 112),self.get_image(16, 112),self.get_image(32, 112)),
           'dead' : self.get_image(48, 64)
       },
    "Slime1" : {
        'down': (self.get_image(0, 0),self.get_image(16, 0), self.get_image(32, 0), self.get_image(48, 0), self.get_image(64, 0), self.get_image(80, 0)),
        'left': (self.get_image(0, 16),self.get_image(16, 16), self.get_image(32, 16), self.get_image(48, 16), self.get_image(64, 16), self.get_image(80, 16)),
        'right': (self.get_image(0, 32),self.get_image(16, 32), self.get_image(32, 32), self.get_image(48, 32), self.get_image(64, 32), self.get_image(80, 32)),
        'up' : (self.get_image(0, 48),self.get_image(16, 48), self.get_image(32, 48), self.get_image(48, 48), self.get_image(64, 48), self.get_image(80, 48)),
        'dead': self.get_image(48, 64)
    },
    "Yeti" : {
        'down': (self.get_image(0, 0),self.get_image(16, 0), self.get_image(32, 0), self.get_image(48, 0), self.get_image(64, 0)),
        'left': (self.get_image(0, 48),self.get_image(16, 48), self.get_image(32, 48), self.get_image(48, 48), self.get_image(64, 48)),
        'right': (self.get_image(0, 32),self.get_image(16, 32), self.get_image(32, 32), self.get_image(48, 32), self.get_image(64, 32)),
        'up': (self.get_image(0, 16),self.get_image(16, 16), self.get_image(32, 16), self.get_image(48, 16), self.get_image(64, 16)),
        'attack_down': (self.get_image(0, 64), self.get_image(16,64), self.get_image(32,64), self.get_image(48, 64), self.get_image(64, 64), self.get_image(80, 64)),
        'attack_up': (self.get_image(0, 80), self.get_image(16,80), self.get_image(32,80), self.get_image(48, 80), self.get_image(64, 80), self.get_image(80, 80)),
        'attack_right': (self.get_image(0, 96), self.get_image(16,96), self.get_image(32,96), self.get_image(48, 96), self.get_image(64, 96), self.get_image(80, 96)),
        'attack_left': (self.get_image(0, 112), self.get_image(16,112), self.get_image(32,112), self.get_image(48, 112), self.get_image(64, 112), self.get_image(80, 112)),
        'dead' : self.get_image(80, 0)
    },
    "SpearGoblin": {
        'down': (self.get_image(0, 0),self.get_image(16, 0), self.get_image(32, 0), self.get_image(48, 0), self.get_image(64, 0)),
        'up': (self.get_image(0, 16),self.get_image(16, 16), self.get_image(32, 16), self.get_image(48, 16), self.get_image(64, 16)),
        'right': (self.get_image(0, 32),self.get_image(16, 32), self.get_image(32, 32), self.get_image(48, 32), self.get_image(64, 32)),
        'left': (self.get_image(0,48),self.get_image(16, 48), self.get_image(32, 48), self.get_image(48, 48), self.get_image(64, 48)),
        'attack_down': (self.get_image(0, 64), self.get_image(0, 96), self.get_image(0, 128)),
        'attack_up': (self.get_image(16, 80), self.get_image(16, 112), self.get_image(16, 144)),
        'attack_right': (self.get_image(32, 112), self.get_image(32, 128), self.get_image(32, 144)),
        'attack_left': (self.get_image(48, 64), self.get_image(48, 80), self.get_image(48, 96)),
        'dead' : self.get_image(80, 0)
    }
}

       self.images = images[type]

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
       self.current_move = 'right'
       self.position[0] += self.walking_speed
       self.change_animation('right')

   def move_left(self):
       self.current_move = 'left'
       self.position[0] -= self.walking_speed
       self.change_animation('left')

   def move_up(self):
       self.current_move = 'up'
       self.position[1] -= self.walking_speed
       self.change_animation('up')

   def move_down(self):
       self.current_move = 'down'
       self.position[1] += self.walking_speed
       self.change_animation('down')

   def move_to(self, position):
       if self.position[0] <= position[0] and abs(self.position[0]- position[0]) >= 5:
           self.move_right()
       if self.position[1] <= position[1] and abs(self.position[1] - position[1]) >= 5:
           self.move_down()
       if self.position[0] >= position[0] and self.position[0] - position[0] >= 5:
           self.move_left()
       if self.position[1] >= position[1] and self.position[1] - position[1] >= 2.5:
           self.move_up()


   def update(self):
       self.rect.topleft = self.position
       self.current_tick += 1
       self.move()
       if self.current_tick > 100:
           self.current_tick = 0

       if self.alive == False:
           if self.current_tick > 99:
               self.tick_revive += 1
               if self.tick_revive == 20:
                   self.tick_revive = 0
                   self.position = [random.randint(init_position[self.type][0],init_position[self.type][1]), random.randint(init_position[self.type][0],init_position[self.type][1])]
                   self.health = self.max_health
                   self.alive = True
                   self.walking = True
                   self.walking_phase = 0
                   self.scored = False

       elif self.attacking == True and self.current_tick % 7 == 0:
           self.attack()
           self.attack_phase += 1
           if self.attack_phase == len(self.images["attack_down"]):
               self.attack_phase = 0
               self.attacking = False
               self.change_animation(self.current_move)

       elif self.walking and self.current_tick % 10 == 0:
           self.walking_phase += 1
           if self.walking_phase == len(self.images["down"]):
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

   def hurted(self, player_damage):
       if self.alive:
           self.health -= player_damage
           if self.current_move == 'down' :
               for _ in range(knockback[self.type]):
                    self.move_up()
           elif self.current_move == 'up':
               for _ in range(knockback[self.type]):
                    self.move_down()
           elif self.current_move == 'right':
               for _ in range(knockback[self.type]):
                   self.move_left()
           else :
               for _ in range(knockback[self.type]):
                   self.move_right()
           if self.health <= 0:
               self.alive = False
               self.walking = False

   def update_health_bar(self, surface, player_pos_x, player_pos_y, screen_size):
       if self.alive :
            pygame.draw.rect(surface, (60, 63, 60), [(self.position[0]-player_pos_x)*2.3+screen_size[0]/2-self.max_health*(5/2), (self.position[1]-player_pos_y)*2.3+screen_size[1]/2-23, self.max_health*5, 5])
            pygame.draw.rect(surface, (111, 210, 46), [(self.position[0]-player_pos_x)*2.3+screen_size[0]/2-self.max_health*(5/2), (self.position[1]-player_pos_y)*2.3+screen_size[1]/2-23, self.health*5, 5])


