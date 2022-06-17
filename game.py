import pygame
import pytmx
import pyscroll
import time
from player import Player
from ennemy import Ennemy
from bonus import Bonus

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("MedhiWar")

        tmx_data = pytmx.util_pygame.load_pygame("assets/MapTemp.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2.3
        self.walls = []

        # On va récupérer tous les objets de la carte
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # générer un player (joueur)
        player_position = tmx_data.get_object_by_name("player_spawn")
        self.player = Player(player_position.x, player_position.y)

        # générer le premier ennemi
        self.all_ennemy = []
        for _ in range(8):
            self.all_ennemy.append(Ennemy("ClubGoblin",1))
        for _ in range(15):
            self.all_ennemy.append(Ennemy("Slime",1))
        for _ in range(0):
            self.all_ennemy.append(Ennemy("Yeti", 1))

        # les bonus :
        self.all_bonus = []
        for _ in range(2):
            self.all_bonus.append(Bonus("heal1"))

        # police des textes
        self.font = pygame.font.Font("assets/my_custom_font.ttf", 25)

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
                           self.all_ennemy[k].scored = True
                       break
        for k in range(len(self.all_ennemy)):
            if abs(self.all_ennemy[k].position[0]-self.player.position[0]) < 120 and abs(self.all_ennemy[k].position[1] - self.player.position[1]) < 120 and self.all_ennemy[k].alive == True :
                self.all_ennemy[k].move_to(self.player.position)
                self.all_ennemy[k].moving_to = True
                self.all_ennemy[k].walking_speed = self.all_ennemy[k].speeds[1]
                if abs(self.all_ennemy[k].position[0]-self.player.position[0]) <= 7 and abs(self.all_ennemy[k].position[1]-self.player.position[1]) <= 7 and abs(time.time()-self.all_ennemy[k].previous_attack_time) > 2 and self.all_ennemy[k].type!="Slime" and self.all_ennemy[k].type!="Yeti":
                    self.all_ennemy[k].attacking = True
                    self.all_ennemy[k].attack()
                    if self.all_ennemy[k].attack_phase == 2:
                        self.player.hurted(self.all_ennemy[k].damage)
                        self.all_ennemy[k].previous_attack_time = time.time()
            else:
                self.all_ennemy[k].moving_to = False
                self.all_ennemy[k].walking_speed = self.all_ennemy[k].speeds[0]
                self.all_ennemy[k].attacking = False
                self.all_ennemy[k].attack_phase = 0

        for k in range(len(self.all_bonus)):
            if abs(self.all_bonus[k].position[0]-self.player.position[0]) < 7 and abs(self.all_bonus[k].position[1] - self.player.position[1]) < 7 and self.all_bonus[k].taken == False:
                self.all_bonus[k].taken = True
                if self.all_bonus[k].type == 'heal1':
                    self.player.heal(2)




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
        if pressed[pygame.K_m]:
            if abs(time.time()-self.player.previous_attack_time) > 0.5:
                self.player.previous_attack_tick = self.player.current_tick
                self.player.previous_attack_time = time.time()
                self.player.attacking = True

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
            self.vie = self.font.render(f'Points de Vie : {self.player.health}', 1, (255,255,255))
            self.screen.blit(self.score_text, (20, 10))
            self.screen.blit(self.vie, (20,40))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
pygame.quit()
