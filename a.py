import pygame, sys, random
from time import sleep

clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Pygame Platformer')

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((600,400))

WINDOW_SIZE = screen.get_size()

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
jump_count = 0
num_moedas = 0
timer = 0
map_c = 3
count_time = 0
real_time = 0

true_scroll = [0,0]

class jumper_obj():
    def __init__(self, loc):
        self.loc = loc  # Use the passed loc parameter

    def render(self, surf, scroll):
        surf.blit(Jumper_image, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))
    
    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 16, 16)
    
    def collision_test(self, rect):
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)

class portal_obj():
    def __init__(self, loc):
        self.loc = loc  # Use the passed loc parameter

    def render(self, surf, scroll):
        surf.blit(Portal_image, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))
    
    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 16, 16)
    
    def collision_test(self, rect):
        portal_rect = self.get_rect()
        return portal_rect.colliderect(rect)

class thorn_obj():
    def __init__(self, loc):
        self.loc = loc  # Use the passed loc parameter

    def render(self, surf, scroll):
        surf.blit(thorn_image, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))
    
    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 16, 16)
    
    def collision_test(self, rect):
        thorn_rect = self.get_rect()
        return thorn_rect.colliderect(rect)

def load_map(path):
    with open('map' + str(path) + '.txt','r') as f:
        data = f.read()
    data = data.split('\n')
    game_map = [list(row) for row in data]
    return game_map

global animation_frames
animation_frames = {}

with open("timer_fase.txt", "w") as f:
    f.write('')

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        if path == 'sprites/Cuei/run' or path == 'sprites/Cuei/idle':
            animation_image.set_colorkey((100,255,100))
        animation_frames[animation_frame_id] = animation_image.copy()
        animation_frame_data.extend([animation_frame_id] * frame)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        
def get_font(size):
    return pygame.font.Font(None, size)

animation_database = {}

animation_database['run'] = load_animation('sprites/Cuei/run',[7,7,7,7,40])
animation_database['idle'] = load_animation('sprites/Cuei/idle',[7,7,7,40])

grass1_img = pygame.image.load('sprites/Grass/Grass1.png')
dirt1_img = pygame.image.load('sprites/Grass/Dirt1.png')
grass2_img = pygame.image.load('sprites/Grass/Grass1.png')
cogV_img = pygame.image.load('sprites/deco/cogumelo1.png')
cogM_img = pygame.image.load('sprites/deco/cogumelo2.png')

thorn_image = pygame.image.load('sprites/thorn.png').convert()
thorn_image.set_colorkey((255,255,255))

Portal_image = pygame.image.load('sprites/jumper.png').convert()
Portal_image.set_colorkey((255,255,255))

Jumper_image = pygame.image.load('sprites/jumper.png').convert()
Jumper_image.set_colorkey((255,255,255))

jump_sound = pygame.mixer.Sound('sound/jump.wav')
jump_sound.set_volume(0.3)
grass_sound = [pygame.mixer.Sound('sound/grass_0.wav'),pygame.mixer.Sound('sound/grass_1.wav')]
grass_sound[0].set_volume(0.1)
grass_sound[1].set_volume(0.1)

pygame.mixer.music.load('sound/music.wav')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

player_action = 'idle'
player_frame = 0
player_flip = False
player_life = 5
can_walk = True

grass_sound_timer = 0

player_rect = pygame.Rect(50,50,16,16)

delay_hit = 0

coin_sprite = pygame.image.load('sprites/coin.png')
image_rect = coin_sprite.get_rect()
image_rect.topleft = (10, 10)

coin_rects = []

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

jumper_objects = []
thorn_objects = []
portal_objects = []
tile_rects = []

y = 0
for layer in load_map(map_c):
    x = 0
    for tile in layer:
        if tile == 'c':
            coin_rect = pygame.Rect(x * 16, y * 16, 16, 16)
            coin_rects.append(coin_rect)
        if tile == 'j':
            jumper_objects.append(jumper_obj((x*16,y*16)))
        if tile == 'T':
            thorn_objects.append(thorn_obj((x*16,y*16)))
        if tile == 'P':
            portal_objects.append(portal_obj((x*16,y*16)))
        if tile in ['1','2','3']:
            tile_rects.append(pygame.Rect(x*16, y*16, 16, 16))
        x += 1
    y += 1

def reset_level(coin_rects_list, map_choice):
    global player_rect, vertical_momentum, air_timer, player_action, player_frame, player_flip, player_life, num_moedas, count_time, real_time, text_timer, timer_text_rect
    coin_rects_list.clear()  # Limpa a lista de moedas
    jumper_objects.clear()
    thorn_objects.clear()
    portal_objects.clear()
    tile_rects.clear()
    coin_positions = set()  # Armazena as posições das moedas para evitar duplicatas
    player_rect = pygame.Rect(50, 50, 16, 16)
    vertical_momentum = 0
    air_timer = 0
    player_action = 'idle'
    player_frame = 0
    player_flip = False
    player_life = 5
    num_moedas = 0
    y = 0
    if map_c <= 3:
        game_map = load_map(map_choice)
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == 'c':
                coin_position = (x * 16, y * 16)  # Posição da moeda
                if coin_position not in coin_positions:  # Verifica se a posição já tem uma moeda
                    coin_rect = pygame.Rect(coin_position[0], coin_position[1], 16, 16)
                    coin_rects_list.append(coin_rect)  # Adiciona moeda à lista
                    coin_positions.add(coin_position)  # Adiciona posição à lista de posições
            if tile == 'j':
                jumper_objects.append(jumper_obj((x*16,y*16)))
            if tile == 'T':
                thorn_objects.append(thorn_obj((x*16,y*16)))
            if tile == 'P':
                portal_objects.append(portal_obj((x*16,y*16)))
            if tile in ['1','2','3']:
                tile_rects.append(pygame.Rect(x*16, y*16, 16, 16))
            x += 1
        y += 1

def collision_test(rect, tiles):
    hit_list = [tile for tile in tiles if rect.colliderect(tile)]
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

# Função para exibir uma caixa de entrada de texto
def get_player_name():
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Se o usuário clicar na caixa de entrada
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                # Muda a cor da caixa de entrada
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Renderiza o texto atual
        txt_surface = font.render(text, True, color)
        # Redimensiona a caixa de entrada se o texto for muito longo
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Desenha a caixa de entrada
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)

    return text
while True:  # Loop principal do jogo
    display.fill((146,244,255))

    #AQUI - Adicione a lógica do jogo aqui

    true_scroll[0] += (player_rect.x-true_scroll[0] - 152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1] - 106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (7,80,75), pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0], background_object[1][1]-scroll[1]*background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14,222,150), obj_rect)
        else:
            pygame.draw.rect(display, (9,91,85), obj_rect)

    tile_rects = []
    y = 0
    for layer in load_map(map_c):
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt1_img, (x*16-scroll[0], y*16-scroll[1]))
            if tile == '2':
                display.blit(grass1_img, (x*16-scroll[0], y*16-scroll[1]))
            if tile == '3':
                display.blit(grass2_img, (x*16-scroll[0], y*16-scroll[1]))
            if tile == '4':
                display.blit(cogV_img, (x*16-scroll[0], y*16-scroll[1]))
            if tile == '5':
                display.blit(cogM_img, (x*16-scroll[0], y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16, y*16, 16, 16))
            x += 1
        y += 1

    if count_time < 60:
        count_time += 1
    else:
        count_time = 0
        real_time += 1

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_life <= 0:
        sleep(1)
        reset_level(coin_rects, map_c)

    player_rect, collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
        jump_count = 0
    else:
        air_timer += 1

    if collisions['top'] == True:
        vertical_momentum = 0
    
    if player_rect.collidelist(coin_rects) != -1:
        num_moedas += 1
        del coin_rects[player_rect.collidelist(coin_rects)]
        print('moeda pega')
    
    player_action,player_frame = change_action(player_action,player_frame,'run' if player_movement[0] != 0 else 'idle')

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
                player_flip = False
            if event.key == K_LEFT:
                moving_left = True
                player_flip = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -4
                    jump_sound.play()
            if event.key == K_DOWN:
                player_rect, collisions = move(player_rect,[0,1],tile_rects)
            if event.key == K_RETURN:
                if player_rect.collidelist([portal_obj.get_rect() for portal_obj in portal_objects]) != -1:
                    map_c += 1
                    reset_level(coin_rects, map_c)
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    if delay_hit > 0:
        delay_hit -= 1
    if player_rect.collidelist([thorn_obj.get_rect() for thorn_obj in thorn_objects]) != -1 and delay_hit == 0:
        player_life -= 1
        delay_hit = 60

    pygame.draw.rect(display, (255,255,255), image_rect)
    for coin_rect in coin_rects:
        display.blit(coin_sprite, (coin_rect.x - scroll[0], coin_rect.y - scroll[1]))
    for portal_obj in portal_objects:
        portal_obj.render(display, scroll)
    for jumper_obj in jumper_objects:
        jumper_obj.render(display, scroll)
    for thorn_obj in thorn_objects:
        thorn_obj.render(display, scroll)

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))

    font = get_font(24)
    text = font.render(f'Moedas: {num_moedas}', True, (255, 255, 255))
    screen.blit(text, (10, 10))

    timer_text = font.render(f'Tempo: {real_time}s', True, (255, 255, 255))
    screen.blit(timer_text, (10, 40))

    life_text = font.render(f'Vida: {player_life}', True, (255, 255, 255))
    screen.blit(life_text, (10, 70))

    pygame.display.update()
    clock.tick(60)
