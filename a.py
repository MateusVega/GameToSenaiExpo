import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Definição de constantes
WINDOW_SIZE = (600, 400)
TILE_SIZE = 16
COIN_SIZE = 16
GRAVITY = 0.2

# Configurações da tela
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Pygame Platformer')

# Carregamento de imagens
grass_img = pygame.image.load('sprites/grass.png')
dirt_img = pygame.image.load('sprites/dirt.png')
coin_sprite = pygame.image.load('sprites/coin.png')
thorn_img = pygame.image.load('sprites/thorn.png').convert()
jumper_img = pygame.image.load('sprites/jumper.png').convert()

# Carregamento de sons
jump_sound = pygame.mixer.Sound('sound/jump.wav')
grass_sound = pygame.mixer.Sound('sound/grass_0.wav')
grass_sound.set_volume(0.1)

# Definição de fonte
font = pygame.font.Font(None, 30)

# Função para carregar o mapa do arquivo de texto
def load_map(path):
    with open(path + '.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    game_map = [list(row) for row in data]
    return game_map

# Função para criar objetos jumper
def create_jumper_objects(game_map):
    jumper_objects = []
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 'j':
                jumper_objects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return jumper_objects

# Função para criar objetos de espinhos
def create_thorn_objects(game_map):
    thorn_objects = []
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 'T':
                thorn_objects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return thorn_objects

# Função para criar retângulos de moedas
def create_coin_rects(game_map):
    coin_rects = []
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 'c':
                coin_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, COIN_SIZE, COIN_SIZE))
    return coin_rects

# Função para mover o jogador
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = [tile for tile in tiles if rect.colliderect(tile)]
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = [tile for tile in tiles if rect.colliderect(tile)]
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

# Carregamento do mapa e criação dos objetos
game_map = load_map('map1')
jumper_objects = create_jumper_objects(game_map)
thorn_objects = create_thorn_objects(game_map)
coin_rects = create_coin_rects(game_map)

# Definição da posição inicial do jogador e variáveis relacionadas
player_rect = pygame.Rect(50, 50, TILE_SIZE, TILE_SIZE)
vertical_momentum = 0
air_timer = 0
num_coins = 0

# Game loop
while True:
    screen.fill((146, 244, 255))

    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == '1':
                screen.blit(dirt_img, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == '2':
                screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))

    for jumper in jumper_objects:
        screen.blit(jumper_img, (jumper.x, jumper.y))

    for thorn in thorn_objects:
        screen.blit(thorn_img, (thorn.x, thorn.y))

    for coin in coin_rects[:]:
        screen.blit(coin_sprite, (coin.x, coin.y))

    # Movimento do jogador
    player_movement = [0, 0]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_movement[0] -= 2
    if keys[pygame.K_d]:
        player_movement[0] += 2
    player_movement[1] += vertical_momentum
    vertical_momentum += GRAVITY

    player_rect, collisions = move(player_rect, player_movement, thorn_objects + jumper_objects)

    if collisions['bottom']:
        vertical_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    if player_rect.y > 400:
        # Reinicia a posição do jogador e das moedas
        player_rect.topleft = (50, 50)
        coin_rects = create_coin_rects(game_map)

    # Colisão do jogador com as moedas
    for coin in coin_rects[:]:
        if player_rect.colliderect(coin):
            num_coins += 1
            coin_rects.remove(coin)

    # Desenho do jogador
    pygame.draw.rect(screen, (255, 0, 0), player_rect)

    # Desenho do número de moedas na tela
    coin_text = font.render(f'Coins: {num_coins}', True, (255, 255, 255))
    screen.blit(coin_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()