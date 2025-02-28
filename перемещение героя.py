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
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = (pos_x + 0.5) * tile_width, (pos_y + 0.5) * tile_height
        self.x, self.y = int(self.rect.x / tile_width), int(self.rect.y / tile_height)
        

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if obj.rect.x < 0:
            obj.rect.x = width - tile_width * (obj.rect.x / tile_width) * -1

        elif obj.rect.x >= width:
            obj.rect.x = 0 + tile_width * ((obj.rect.x - width) / tile_width) 

        if obj.rect.y < 0:
            obj.rect.y = height - tile_width * (obj.rect.y / tile_height) * -1

        elif obj.rect.y >= height:
            obj.rect.y = 0 + tile_height * ((obj.rect.y - height) / tile_height)

        obj.rect.x += self.dx
        obj.rect.y += self.dy
    
    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.centerx- width // 2)
        self.dy = -(target.rect.centery - height // 2)
        

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

    width, height = len(level[0]) * tile_width, len(level) * tile_height

    screen = pygame.display.set_mode((width, height))

    clock = pygame.time.Clock()
    camera = Camera()
    player, level_x, level_y = generate_level(level)
    running = True

    start_screen()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                x, y = player.x, player.y

                if event.key == pygame.K_w:
                    y -= 1

                    if y < 0:
                        y = len(level) - 1
                                        
                    if level[y][x] != '#':
                        player.rect.y -= tile_height
                        player.y -= 1

                        if player.y < 0:
                            player.y = y

                if event.key == pygame.K_a:
                    x -= 1
                    
                    if x < 0:
                        x = len(level[y]) - 1
                    
                    if level[y][x] != '#':
                        player.rect.x -= tile_width
                        player.x -= 1

                        if player.x < 0:
                            player.x = x
                
                if event.key == pygame.K_s:
                    y += 1

                    if y > len(level) - 1:
                            y = 0
                    
                    if level[y][x] != '#':
                        player.rect.y += tile_height
                        player.y += 1


                        if player.y > len(level) - 1:
                            player.y = 0


                if event.key == pygame.K_d:
                    x += 1
                    
                    if x > len(level[y]) - 1:
                        x = 0
                    
                    if level[y][x] != '#':
                        player.rect.x += tile_width
                        player.x += 1

                        if player.x > len(level[y]) - 1:
                            player.x = 0
        
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)


        screen.fill(pygame.color.Color('black'))
        tiles_group.update()
        tiles_group.draw(screen)
        player_group.update()
        player_group.draw(screen)
        pygame.display.flip()

    terminate()