import pygame
import pytmx
import pyscroll
import time
import json

from player import Player
from ennemy import Ennemy
from bonus import Bonus

class Game:

    def __init__(self):

        self.best_scores = json.load(open('assets/indexes/scores.json', 'r'))

        self.screen = pygame.display.set_mode((1366, 768))
        pygame.display.set_caption("MedhiWar")
        pygame.display.set_icon(pygame.image.load("assets/sword_02c.ico"))
        tmx_data = pytmx.util_pygame.load_pygame("assets/MapTemp.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2.3
        self.walls = []
        self.help = False
        self.speed_timer = time.time()

        # On va récupérer tous les objets de la carte
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # générer un player (joueur)
        player_position = tmx_data.get_object_by_name("player_spawn")
        self.player = Player(player_position.x, player_position.y)

        # générer le premier ennemi
        self.all_ennemy = []
        for _ in range(4):
            self.all_ennemy.append(Ennemy("ClubGoblin"))
        for _ in range(30):
            self.all_ennemy.append(Ennemy("Slime1"))
        for _ in range(0):
            self.all_ennemy.append(Ennemy("Yeti"))
        for _ in range(4):
            self.all_ennemy.append(Ennemy("SpearGoblin"))

        # les bonus :
        self.all_bonus = []
        for _ in range(1):
            self.all_bonus.append(Bonus("heal1"))
        for _ in range(1):
            self.all_bonus.append(Bonus("speed1"))

        # police des textes
        self.font = pygame.font.Font("assets/my_custom_font.ttf", 25)
        self.font2 = pygame.font.Font("assets/my_custom_font.ttf", 15)

         # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=1)
        self.group.add(self.player)
        self.group.add(self.all_ennemy)
        self.group.add(self.all_bonus)

    def update(self):
        self.group.update()
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
        if self.player.attack_phase == 4:
               self.player.attacking = False
               self.player.attack()
               self.player.attack_phase = 0
               for k in range(len(self.all_ennemy)):
                   if abs(self.all_ennemy[k].position[0]-self.player.position[0]) < 15 and abs(self.all_ennemy[k].position[1]-self.player.position[1]) <15 and self.all_ennemy[k].alive == True:
                       self.all_ennemy[k].hurted(self.player.damage)
                       if self.all_ennemy[k].alive == False and self.all_ennemy[k].scored == False:
                           self.player.add_score(self.all_ennemy[k].score_given)
                           self.player.add_xp(self.all_ennemy[k].score_given, self.screen.get_size())
                           self.all_ennemy[k].scored = True
                       break
        for k in range(len(self.all_ennemy)):
            if abs(self.all_ennemy[k].position[0]-self.player.position[0]) < 120 and abs(self.all_ennemy[k].position[1] - self.player.position[1]) < 120 and self.all_ennemy[k].alive == True :
                self.all_ennemy[k].move_to(self.player.position)
                self.all_ennemy[k].moving_to = True
                self.all_ennemy[k].walking_speed = self.all_ennemy[k].speeds[1]
                if abs(self.all_ennemy[k].position[0]-self.player.position[0]) <= 7 and abs(self.all_ennemy[k].position[1]-self.player.position[1]) <= 7 and abs(time.time()-self.all_ennemy[k].previous_attack_time) > self.all_ennemy[k].attack_speed and self.all_ennemy[k].type != "Slime1":
                        self.all_ennemy[k].attacking = True
                        self.all_ennemy[k].attack()
                        if self.all_ennemy[k].attack_phase == len(self.all_ennemy[k].images['attack_down'])-1:
                            self.player.hurted(self.all_ennemy[k].damage)
                            self.all_ennemy[k].previous_attack_time = time.time()
            else:
                self.all_ennemy[k].moving_to = False
                self.all_ennemy[k].walking_speed = self.all_ennemy[k].speeds[0]
                self.all_ennemy[k].attacking = False
                self.all_ennemy[k].attack_phase = 0

        for k in range(len(self.all_bonus)):
            if abs(self.all_bonus[k].position[0]-self.player.position[0]) < 10 and abs(self.all_bonus[k].position[1] - self.player.position[1]) < 10 and self.all_bonus[k].taken == False:
                self.all_bonus[k].taken = True
                if self.all_bonus[k].type == 'heal1':
                    self.player.heal(2)
                elif self.all_bonus[k].type == "speed1":
                    self.player.speed = 6
                    self.speed_timer = time.time()



    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_z]:
            self.player.walking = True
            self.player.move_up()
        elif pressed[pygame.K_s]:
            self.player.walking = True
            self.player.move_down()
        elif pressed[pygame.K_q]:
            self.player.walking = True
            self.player.move_left()
        elif pressed[pygame.K_d]:
            self.player.walking = True
            self.player.move_right()
        if not(pressed[pygame.K_d]) and not(pressed[pygame.K_q]) and not(pressed[pygame.K_z]) and not(pressed[pygame.K_s]):
            self.player.walking = False
        if pressed[pygame.K_SPACE]:
            if abs(time.time()-self.player.previous_attack_time) > 0.5:
                self.player.previous_attack_tick = self.player.current_tick
                self.player.previous_attack_time = time.time()
                self.player.attacking = True
        if pressed[pygame.K_a]:
            self.help = True
        elif not(pressed[pygame.K_a]):
            self.help = False


    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.player.save_location()
            for k in range(len(self.all_ennemy)):
                self.all_ennemy[k].save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            self.score_text = self.font.render(f"Score : {self.player.score_value}", 1, (255, 255, 255))
            self.screen.blit(self.score_text, (20, 10))
            self.level_text = self.font.render(f"Level : {self.player.level}", 1, (255, 255, 255))
            self.screen.blit(self.level_text, (20, 40))
            self.help_text = self.font2.render(f"Help : A", 1, (255, 255, 255))
            self.screen.blit(self.help_text, (self.screen.get_size()[0]-80,10))
            if self.help == True :
                self.help_text1 = self.font2.render(f"Z,Q,S,D : move", 1, (255, 255, 255))
                self.screen.blit(self.help_text1, (self.screen.get_size()[0]-130, 40))
                self.help_text2 = self.font2.render(f"SPACE : fight", 1, (255, 255, 255))
                self.screen.blit(self.help_text2, (self.screen.get_size()[0]-130, 60))
            self.player.update_bar(self.screen, self.screen.get_size(), self.speed_timer)
            if self.player.speed >= 6 and time.time() - self.speed_timer > 5 :
                self.player.speed = self.player.init_speed
            for k in range(len(self.all_ennemy)):
                self.all_ennemy[k].update_health_bar(self.screen, self.player.position[0], self.player.position[1], self.screen.get_size())
            pygame.display.flip()
            if self.player.health <= 0:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if running == False :
                self.best_scores["Max"] = self.player.score_value
                print('Score :', self.best_scores['Max'])
                json.dump(self.best_scores, open('assets/indexes/scores.json', 'w'), indent=2)
            clock.tick(60)

pygame.quit()
print("Merci d'avoir joué")
