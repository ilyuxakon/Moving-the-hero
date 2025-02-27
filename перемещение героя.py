import pygame
import sys


FPS = 50


tile_images = {
    'wall': pygame.image.load('image/box.png'),
    'empty': pygame.image.load('image/grass.png')
}
player_image = pygame.image.load('image/mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        
def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(pygame.image.load('image/fon.jpg'), (550, 550))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    try:
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину    
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')    
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    
    except Exception:
        return False


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках            
    return new_player, x, y


if __name__ == '__main__':
    name = input()
    level = load_level(name)

    if not level:
        print('Ошибка')
        terminate()

    pygame.init()
    screen = pygame.display.set_mode((len(level[0]) * tile_width, len(level) * tile_height))

    clock = pygame.time.Clock()
    player, level_x, level_y = generate_level(level)
    running = True

    start_screen()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                x, y = int(player.rect.x / tile_width), int(player.rect.y / tile_height)
                
                if event.key == pygame.K_w:
                    y -= 1
                    
                    if y >= 0 and level[y][x] != '#':
                        player.rect.y -= tile_height

                if event.key == pygame.K_a:
                    x -= 1
                    
                    if x >= 0 and level[y][x] != '#':
                        player.rect.x -= tile_width
                
                if event.key == pygame.K_s:
                    y += 1
                    
                    if y < len(level) and level[y][x] != '#':
                        player.rect.y += tile_height

                if event.key == pygame.K_d:
                    x += 1
                    
                    if x < len(level[y]) and level[y][x] != '#':
                        player.rect.x += tile_width
        
        screen.fill(pygame.color.Color('black'))
        tiles_group.update()
        tiles_group.draw(screen)
        player_group.update()
        player_group.draw(screen)
        pygame.display.flip()

    terminate()