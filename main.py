import pygame
from pygame import mixer
import os
import csv
import random

#Initialisation des modules
mixer.init()
pygame.init()
#Initialisation de la fenêtre
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Project")

#Background
BG = (221, 198, 161)

#Mode debug
debug_mode = False

#Gravité
gravity = 0.85

#Liste de Texture
dico_texture = {
    1 : "Default",
    2 : "Mario",
}
current_texture_index = 1
texture_nom = dico_texture[current_texture_index]

death_sound_counter = 1

#Scrolling du jeu
scroll_thresh = 200
screen_scroll = 0
bg_scroll = 0

#Taille de la carte en CSV
lignes = 20
colonne = 151

#Score du Jeu
score = 0

#Taille et type de chaque tuile
tile_size = 32
tile_type = len(os.listdir('Default/Asset_game/Terrain'))

#Le numéro du level
level = 2
max_level = 2

start_game = False
option_active = False
start_intro = False
#charge la musique
pygame.mixer.music.load(f'{texture_nom}/Audio/Musique.mp3')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1, 0.0)

def update_musique(texture_nom):
    pygame.mixer.music.load(f'{texture_nom}/Audio/Musique.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1, 0.0)

def update_sfx(texture_nom):
    jump = pygame.mixer.Sound(f'{texture_nom}/Audio/Jump.mp3')
    damage = pygame.mixer.Sound(f'{texture_nom}/Audio/Hit.mp3')
    piece = pygame.mixer.Sound(f'{texture_nom}/Audio/Piece.mp3')
    end = pygame.mixer.Sound(f'{texture_nom}/Audio/End.mp3')
    death = pygame.mixer.Sound(f'{texture_nom}/Audio/Death.mp3')

    jump.set_volume(0.5)
    damage.set_volume(0.5)
    piece.set_volume(0.25)
    end.set_volume(1)
    death.set_volume(0.5)

    return jump, damage, piece, end, death

jump_sfx, damage_sfx, piece_sfx, end_sfx, death_sfx = update_sfx(texture_nom)

start_img = pygame.image.load('Button/Play/play01.png').convert_alpha()
restart_img = pygame.image.load('Button/Restart/restart01.png').convert_alpha()
option_img1 = pygame.image.load('Button/Option/option01.png').convert_alpha()



#Chargement de toutes les images pour le fond
img_bg1_d = pygame.image.load(f'Default/Asset_game/BackGround/BG Image (1).png').convert_alpha()
img_bg2_d = pygame.image.load('Default/Asset_game/BackGround/Big Clouds.png').convert_alpha()
img_bg3_d = pygame.image.load('Default/Asset_game/BackGround/Small Cloud 2.png').convert_alpha()
img_bg4_d = pygame.image.load('Default/Asset_game/BackGround/Small Cloud 3.png').convert_alpha()

img_bg_m = pygame.image.load('Mario/Asset_game/BackGround/backgrounds1.png')

#Chargement de toutes les images des tuiles
font = pygame.font.SysFont('Arial', 30)

def Debug_mode():
    pygame.draw.rect(screen, (0, 255, 0), player.rect, 2)
    pygame.draw.rect(screen, (0, 255, 0), enemy.rect, 2)
    pygame.draw.rect(screen, (0, 255, 0), sortie.rect, 2)
    pygame.draw.rect(screen, (0, 255, 0), piece.rect, 2)
    Draw_text(f'X : {player.rect.x}', font, (255, 0, 0), 0, 0)
    Draw_text(f'Y : {player.rect.y}', font, (255, 0, 0), 0, 25)
    Draw_text(f"Point de vie : {player.health}", font, (255, 0, 0), 0, 100)
    Draw_text(f"Score : {score}", font, (255, 0, 0), 0, 120)
    Draw_text(f"{int(clock.get_fps())}", font,(255, 0, 0), 700, 0)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


#Dessin du fond
def draw_bg(texture_nom):
    screen.fill(BG)
    for x in range(100):
        if texture_nom == "Default":
            screen.blit(img_bg1_d, ((x * img_bg1_d.get_width()) - bg_scroll, 600 - img_bg1_d.get_height()))
            screen.blit(img_bg2_d, ((x * img_bg2_d.get_width()) - bg_scroll * 0.5, 600 - img_bg2_d.get_height() - 109))
            screen.blit(img_bg2_d, ((x * img_bg3_d.get_width()) - bg_scroll * 0.6, 600 - img_bg2_d.get_height() - 115))
            screen.blit(img_bg3_d, ((x * img_bg3_d.get_width() * 6) - bg_scroll * 0.4, 600 - img_bg3_d.get_height() - 424))
            screen.blit(img_bg3_d, ((x * img_bg3_d.get_width() * 6) - bg_scroll * 0.4, 200 - img_bg3_d.get_height() - 442))
            screen.blit(pygame.transform.flip(img_bg3_d, True, False), (((x * img_bg3_d.get_width() * 6) - bg_scroll * 0.55) - 200, 325 - img_bg2_d.get_height() - 481))
            screen.blit(img_bg4_d, (((x * img_bg4_d.get_width() * 6) - bg_scroll * 0.7) - 200, 600 - img_bg2_d.get_height() - 431))
            screen.blit(img_bg4_d, (((x * img_bg4_d.get_width() * 6) - bg_scroll * 0.75) - 325, 600 - img_bg2_d.get_height() - 261))
            screen.blit(pygame.transform.flip(img_bg4_d, True, False), (((x * img_bg3_d.get_width() * 6) - bg_scroll * 0.65) - 200, 600 - img_bg2_d.get_height() - 347))
        elif texture_nom == "Mario":
            screen.blit(img_bg_m, ((x * img_bg_m.get_width()) - bg_scroll* 0.7, 600 - img_bg_m.get_height()))


def Draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def reset_level():
    enemy_group.empty()
    decoration_group.empty()
    sortie_group.empty()
    piece_group.empty()

    data = []

    for row in range(lignes):
        r = [-1] * colonne
        data.append(r)

    return data


#Classe du joueur ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    #Initialisation de toutes, les variables, les images, des collisions du Joueur
    def __init__(self, type, x, y, scale, speed, dico_textures):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.texture = 1
        self.dico_texture = dico_textures
        self.health = 3
        self.max_health = self.health
        self.damage_cooldown = 0
        self.score = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.type = type
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #Variable pour l'IA
        self.move_counter = 0
        self.idling = False
        self.idling_counter =0
        #Charge toutes les images du joueur pour l'animation
        animation_types = ['Idle', 'Run', 'Jump', 'Dead']
        for animation in animation_types:
            temp_list =[]
            number_of_frames = len(os.listdir(f"{dico_textures[self.texture]}/{self.type}/{animation}"))
            for i in range(number_of_frames):
                img = pygame.image.load(f"{dico_textures[self.texture]}/{self.type}/{animation}/{animation} {i}.png")
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    #Mouvement du Joueur
    def move(self, moving_left, moving_right):

        screen_scroll = 0
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1


        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = self.vel_y
        dy += self.vel_y

        for tile in world.obstacle_list:
             if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                 dx = 0
             if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                 if self.vel_y < 0:
                    self.vel_y = 0
                    dy =  tile[1].bottom - self.rect.top
                 elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy =  tile[1].top - self.rect.bottom

        level_complete = False
        if pygame.sprite.spritecollide(self, sortie_group, False):
            level_complete = True

        if self.rect.bottom > 600:
            self.health = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.type == 'Player':
            if (self.rect.right > 800 - scroll_thresh and bg_scroll < (world.level_length * tile_size) - 800) \
                    or (self.rect.left < scroll_thresh and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx


        return screen_scroll, level_complete

    def IA(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 150) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 200

            if self.idling == False:
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right)
                self.update_action(1)
                self.move_counter += 1

                if self.move_counter > tile_size:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False

        self.rect.x += screen_scroll
    #Mise à jour du joueur
    def update_animation(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    #Mise à jour des actions
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_rect(self):
        # Met à jour le rect et les dimensions du joueur
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update_texture(self, new_texture):
        if new_texture != self.texture:
            self.texture = new_texture
            self.animation_list = []
            animation_types = ['Idle', 'Run', 'Jump', 'Dead']
            for animation in animation_types:
                temp_list = []
                number_of_frames = len(os.listdir(f"{self.dico_texture[self.texture]}/{self.type}/{animation}"))
                for i in range(number_of_frames):
                    img = pygame.image.load(
                        f"{self.dico_texture[self.texture]}/{self.type}/{animation}/{animation} {i}.png")
                    scale_factor = 2  # Ajuste ici si tu veux rendre tous les skins plus grands/petits
                    img = pygame.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

            # Réinitialise l'image et mets à jour le rect
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.image = self.animation_list[self.action][self.frame_index]
            self.update_rect()



    def update(self):
        self.update_animation()
        self.check_alive()
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        if pygame.sprite.spritecollide(player, enemy_group, False) and player.alive:
            player.damage()


    def damage(self):
        if self.damage_cooldown == 0:
            self.damage_cooldown = 100
            self.health -= 1
            damage_sfx.play()

    def check_alive(self):
        if self.health == 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)



    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Classe Barre de vie -----------------------------------------------------------------------------------------------------------------------------

class Bar_de_vie():
    def __init__(self, x, y,  health, scale,):
        self.x= x
        self.y = y
        self.health = health
        self.scale = scale
        image = pygame.image.load(f'Health Heart/Health {self.health}.png').convert_alpha()
        image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.image = image
        self.rect = self.image.get_rect()

    def update_health(self, health):
        self.new_health = health
        self.image = pygame.image.load(f'Health Heart/Health {self.new_health}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, False, False), self.rect)

#Classe Decoration -----------------------------------------------------------------------------------------------------------------------------

class Decoration(pygame.sprite.Sprite):
    def __init__(self, animation_type, scale, x, y, ):
        pygame.sprite.Sprite.__init__(self)
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.frame_index = 0
        animation_types = animation_type
        for animation in animation_types:
            temp_list = []
            number_of_frames = len(os.listdir(f"{texture_nom}/Asset_game/Decoration/{animation_types}"))
            for i in range(number_of_frames):
                img = pygame.image.load(f"{texture_nom}/Asset_game/Decoration/{animation_types}/{animation_types} {i}.png")
                img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[0][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        animation_cooldown = 150
        self.image = self.animation_list[0][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[0]):
            self.frame_index = 0
        self.rect.x += screen_scroll

    def update_texture(self, new_texture):
        if new_texture != self.texture:
            self.texture = new_texture
            self.animation_list = []
            animation_types = ['Idle', 'Run', 'Jump', 'Dead']
            for animation in animation_types:
                temp_list = []
                number_of_frames = len(os.listdir(f"{self.dico_texture[self.texture]}/{self.type}/{animation}"))
                for i in range(number_of_frames):
                    img = pygame.image.load(
                        f"{self.dico_texture[self.texture]}/{self.type}/{animation}/{animation} {i}.png")
                    scale_factor = 1.5  # Ajuste ici si tu veux rendre tous les skins plus grands/petits
                    img = pygame.transform.scale(img, (
                        int(img.get_width() * scale_factor), int(img.get_height() * scale_factor)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

            # Réinitialise l'image et mets à jour le rect
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.image = self.animation_list[self.action][self.frame_index]
            self.update_rect()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, False, False), self.rect)


#Classe de Piece ---------------------------------------------------------------------------------------------------------

class Piece(pygame.sprite.Sprite):
    def __init__(self,scale, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.frame_index = 0
        temp_list = []
        number_of_frames = len(os.listdir(f"{texture_nom}/Asset_game/Piece"))
        for i in range(number_of_frames):
            img = pygame.image.load(f"{texture_nom}/Asset_game/Piece/Piece {i}.png")
            img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[0][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        animation_cooldown = 100
        self.image = self.animation_list[0][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[0]):
            self.frame_index = 0
        self.rect.x += screen_scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, False, False), self.rect)

#Classe de Sortie ----------------------------------------------------------------------------------------------------
class Sortie(pygame.sprite.Sprite):
    def __init__(self,scale, x, y, dico_texture):
        pygame.sprite.Sprite.__init__(self)
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.texture = dico_texture[current_texture_index]
        self.frame_index = 0
        temp_list = []
        number_of_frames = len(os.listdir(f"{texture_nom}/Asset_game/Sortie"))
        for i in range(number_of_frames):
            img = pygame.image.load(f"{texture_nom}/Asset_game/Sortie/Flag {i}.png")
            img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[0][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        animation_cooldown = 150
        self.image = self.animation_list[0][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[0]):
            self.frame_index = 0
        self.rect.x += screen_scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, False, False), self.rect)

# Classe du bouton -----------------------------------------------------------------------------------------------------------------------------

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

enemy_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
piece_group = pygame.sprite.Group()

class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.colour, (0- self.fade_counter, 0, 800 //2, 600))
            pygame.draw.rect(screen, self.colour, (800 //2 + self.fade_counter, 0, 800, 600))
            pygame.draw.rect(screen, self.colour, (0, 0- self.fade_counter, 800, 600))
            pygame.draw.rect(screen, self.colour, (0, 600 //2 + self.fade_counter, 800, 600))
        if self.direction == 2:
            pygame.draw.rect(screen, self.colour, (0, 0, 800, 0 + self.fade_counter))
        if self.fade_counter >= 600:
            fade_complete = True

        return fade_complete

intro_fade = ScreenFade(1, (0, 0, 0), 4)
death_fade = ScreenFade(2, (255, 0, 0), 4)

def update_texture_tile(texture_nom):
    img_list = []
    for x in range(tile_type):
        img = pygame.image.load(f'{texture_nom}/Asset_game/Terrain/{x}.png').convert_alpha()
        img = pygame.transform.scale(img, (tile_size, tile_size))
        img_list.append(img)
    return img_list

img_list = update_texture_tile(dico_texture[current_texture_index])
# Classe de la carte --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class World():
    #Initialisation des variables
    def __init__(self):
        self.obstacle_list =[]
        self.transparent_list = []

    #Les données comme position de chaque tuile, type de chaque tuile du tableau csv sont sur le jeu
    def process_data(self, data):
        self.level_length = len(data[0])
        for y, ligne in enumerate(data):
            for x, tile in enumerate(ligne):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * tile_size
                    img_rect.y = y * tile_size
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 53:
                        self.obstacle_list.append(tile_data)
                    if tile == 54:
                        self.transparent_list.append(tile_data)
                    if tile >= 55 and tile <= 84:
                        self.obstacle_list.append(tile_data)
                    if tile == 85:
                        player = Player("Player", x*tile_size, y*tile_size, 1.75, 5, dico_texture)
                        barre_de_vie = Bar_de_vie(150, 0, player.health, 3)
                    if tile == 86:
                        enemy = Player("Enemy", x*tile_size, y*tile_size, 1.65, 2, dico_texture)
                        enemy_group.add(enemy)
                    if tile == 87:
                        decoration = Decoration("Arbre_milieu", 2, x*tile_size, (y*tile_size)-30)
                        decoration_group.add(decoration)
                    if tile == 88:
                        sortie = Sortie(2, x*tile_size, (y*tile_size)-60, dico_texture)
                        sortie_group.add(sortie)
                    if tile == 89:
                        piece = Piece(2, x*tile_size, y*tile_size)
                        piece_group.add(piece)

        return player, barre_de_vie
    #Dessin de chaque tuile
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        for tile in self.transparent_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


start_button = Button(800 // 2 - 150, 600 //2 - 120, start_img, 2)
restart_button = Button(800 // 2 - 150, 600 // 2 - 150, restart_img, 2)



enemy_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
sortie_group = pygame.sprite.Group()
#Groupe tous les ennemis

#Initialisation d'une carte
world_data = []
for row in range(lignes):
    r = [-1] * colonne
    world_data.append(r)

#Ouvre le tableau csv qui est la carte
def Carte_csv():
    with open(f'Niveau/Niveau {level}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, ligne in enumerate(reader):
            for y, tile in enumerate(ligne):
                world_data[x][y] = int(tile)
    return world_data

world_data = Carte_csv()
#Appel de toutes les classes (World, Player)---------------------------------------------------------------------------------------------------------------------------------------
run = True

try:
    world = World()
    player, barre_de_vie = world.process_data(world_data)
except UnboundLocalError:
    print("Le joueur n'est pas placé")
    run = False

#Le nombre de Frame Par Seconde
clock = pygame.time.Clock()
FPS = 60


moving_left = False
moving_right = False

#Une boucle qui fait tourner le jeu ---------------------------------------------------------------------------------------------------------------------------------------

while run:
    clock.tick(FPS)

    if start_game == False:
        screen.fill(BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True

    else:
        draw_bg(dico_texture[current_texture_index])
        world.draw()
        for decoration in decoration_group:
            decoration.update_animation()
            decoration.draw()

        for piece in piece_group:
            piece.update_animation()
            piece.draw()

        for sortie in sortie_group:
            sortie.update_animation()
            sortie.draw()


        player.update()
        player.draw()
        barre_de_vie.update_health(player.health)
        barre_de_vie.draw()

        for enemy in enemy_group:
            enemy.IA()
            enemy.update_animation()
            enemy.draw()

        if debug_mode:
            Debug_mode()

        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0


        if player.alive:
            if pygame.sprite.spritecollide(player, piece_group, True):
                score += 1
                piece_sfx.play()
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            if level_complete:
                end_sfx.play()
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= max_level:
                    with open(f'Niveau/Niveau {level}.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, ligne in enumerate(reader):
                            for y, tile in enumerate(ligne):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, barre_de_vie = world.process_data(world_data)
                    player, barre_de_vie = world.process_data(world_data)
                    player.update_texture(current_texture_index)
                    texture_nom = dico_texture[current_texture_index]

                    jump_sfx, damage_sfx, piece_sfx, end_sfx, death_sfx = update_sfx(texture_nom)

        else:
            screen_scroll = 0
            if death_sound_counter > 0:
                death_sfx.play()
                death_sound_counter -= 1
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    player.update_texture(2)
                    score = 0
                    bg_scroll = 0
                    world_data = reset_level()
                    with open(f'Niveau/Niveau {level}.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, ligne in enumerate(reader):
                            for y, tile in enumerate(ligne):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, barre_de_vie = world.process_data(world_data)
                    player.update_texture(current_texture_index)
                    texture_nom = dico_texture[current_texture_index]

                    jump_sfx, damage_sfx, piece_sfx, end_sfx; death_sfx = update_sfx(texture_nom)
                    update_musique(texture_nom)



    #Permet de quitter la boucle donc le jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #Les commandes des mouvements du joueur
        if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_q or event.key == pygame.K_LEFT:
                moving_left = True
            if (event.key == pygame.K_z or event.key == pygame.K_SPACE or event.key == pygame.K_UP)\
                    and player.alive and player.in_air == False:
                player.jump = True
                jump_sfx.play()
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_g:
                debug_mode = True
            if event.key == pygame.K_i:
                current_texture_index += 1
                if current_texture_index > len(dico_texture):
                    current_texture_index = 1
                bg_scroll = 0
                score = 0
                texture_nom = dico_texture[current_texture_index]
                world_data = reset_level()
                world_data = Carte_csv()

                barre_de_vie.update_health(player.health)
                barre_de_vie.draw()

                img_list = update_texture_tile(texture_nom)

                for sortie in sortie_group:
                    sortie.update_animation()
                    sortie.draw()

                world = World()
                player, barre_de_vie = world.process_data(world_data)

                player.update_texture(current_texture_index)

                jump_sfx, damage_sfx, piece_sfx, end_sfx, death_sfx = update_sfx(texture_nom)
                update_musique(texture_nom)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_q or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_g:
                debug_mode = False
    pygame.display.update()
pygame.quit()


