from pygame import *
from random import randint

window = display.set_mode((1500, 1000))

display.set_caption('Ping-pong')

background = transform.scale(image.load('background.jpg'), (1500, 1000))
FPS = 80
clock = time.Clock()
game = True
finish = True

mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()
kick = mixer.Sound('ball_from_rocket.mp3')
bounce = mixer.Sound('ball_from_table.mp3')
num_l = 0
num_w = 0
font.init()
font = font.SysFont('Arial', 70)
win_1 = font.render('Выиграл игрок 1!!!', True, (204,0,0))
win_2 = font.render('Выиграл игрок 2!!!', True, (204,0,0))


class GameSprite(sprite.Sprite):
    def __init__(self, player_speed, player_x, player_y, player_image, length, width):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (length, width))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Rocket(GameSprite):
    def update(self, K1, K2):
        if keys_pressed[K1] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K2] and self.rect.y < 800:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_speed, player_x, player_y, player_image,length, width):
        super().__init__(player_speed, player_x, player_y, player_image,length, width)
        self.speed_x = 4
        self.speed_y = 4
        self.wait = 0
    def update(self):
        if self.rect.y <= 0 or self.rect.y >= 900:
            self.speed_y *= -1
            bounce.play()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.wait % 1000 == 0:
            self.speed_x += 1
            self.speed_y += 1
        self.wait += 1 

p1 = Rocket(4, 100, 500, 'platform.jpg', 40, 200)
p2 = Rocket(4, 1400, 500, 'platform.jpg', 40, 200)
b1 = Ball(2, randint(400, 500), randint(100,900),'ball.png', 100, 100)
characters = sprite.Group()
characters.add(p1, p2)

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish:
        keys_pressed = key.get_pressed()
        window.blit(background, (0, 0))
        characters.draw(window)
        p1.update(K_w, K_s)
        p2.update(K_UP, K_DOWN)
        b1.reset()
        b1.update()

        if b1.rect.x <= 0:
            b1.rect.x = randint(400, 500)
            b1.rect.y = randint(0,900)
            num_l += 1
        if b1.rect.x >= 1400:
            b1.rect.x = randint(400, 500)
            b1.rect.y = randint(0,900)
            num_w += 1


        if sprite.spritecollide(b1, characters, False):
            b1.speed_x *= -1
            kick.play()
        num_1 = font.render(str(num_w), True, (204,0,0))
        num_2 = font.render(str(num_l), True, (204,0,0))
        window.blit(num_1, (1300,100))
        window.blit(num_2,(100,100))
        if num_w == 3:
            window.blit(win_1, (600,500))
            finish = False
        if num_l == 3:
            window.blit(win_2, (600,500))
            finish = False


    clock.tick(FPS)
    display.update()
