from random import choice

from pygame import *
mixer.init()
init()
font.init()


class GameSprite (sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        virtual_surface.blit(self.image, (self.rect.x, self.rect.y))


class Ball(GameSprite):
    def __init__(self):
        super().__init__("images/ball.png", WIDTH // 2 - 25, HEIGHT // 2 - 25, 56, 58, 10)
        self.speed_x = self.speed
        self.speed_y = self.speed
        self.disabled = True
        self.wait = 30

    def update(self):
        global score_player_1, score_player_2, text_score_1, text_score_2

        if not self.disabled:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if self.rect.y >= HEIGHT - self.rect.height:
                self.speed_y *= -1
            if self.rect.y <= 0:
                self.speed_y *= -1

            if sprite.collide_rect(self, player_1):
                self.speed_x *= -1.85
                self.rect.x += 18

            if sprite.collide_rect(self, player_2):
                self.speed_x *= -1.05
                self.rect.x -= 10

            if self.rect.x >= WIDTH:
                score_player_1 += 1
                text_score_1 = font_interface.render(str(score_player_1), True, (0, 0, 0))
                self.respawn()

            if self.rect.x <= self.rect.width:
                score_player_2 += 1
                text_score_2 = font_interface.render(str(score_player_2), True, (0, 0, 0))
                self.respawn()
        else:
            self.wait -= 1
            if self.wait <= 0:
                self.disabled = False

    def respawn(self):
        self.rect.x = WIDTH // 2 - 25
        self.rect.y = HEIGHT // 2 - 25
        self.speed_x = choice((-10, 10))
        self.speed_y = choice((-10, 18))
        self.disabled = True
        self.wait = 30


class Platform(GameSprite):
    def __init__(self, player_num):
        self.player_num = player_num
        if self.player_num == 1:
            self.x = 100
            self.angle = - 90
        if self.player_num == 2:
            self.x = 1120
            self.angle = 90
        super().__init__("images/platform.png", 0, 0, 150, 20, 15)
        self.image = transform.rotate(self.image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = HEIGHT // 2 - 75

    def update(self):
        keys_pressed = key.get_pressed()

        if self.player_num == 1:
            if keys_pressed[K_w] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys_pressed[K_s] and self.rect.y < HEIGHT - self.rect.height:
                self.rect.y += self.speed

        if self.player_num == 2:
            if keys_pressed[K_UP] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys_pressed[K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
                self.rect.y += self.speed


WIDTH = 1280
HEIGHT = 720

ASPECT_RATIO = WIDTH / HEIGHT

window = display.set_mode((WIDTH, HEIGHT), RESIZABLE)
display.set_caption("Ping-pong")
clock = time.Clock()

virtual_surface = Surface((WIDTH, HEIGHT))
current_size = window.get_size()

ball = Ball()

player_1 = Platform(1)
player_2 = Platform(2)

score_player_1 = 0
score_player_2 = 0

font_interface = font.Font(None, 70)
font_finish = font.Font(None, 200)

text_score_1 = font_interface.render(str(score_player_1), True, (0, 0, 0))
text_score_2 = font_interface.render(str(score_player_2), True, (0, 0, 0))

win_1 = font_finish.render("Win Player 1", True, (0, 0, 0))
win_2 = font_finish.render("Win Player 2", True, (0, 0, 0))

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
            if e.key == K_r:
                ball.rect.x = WIDTH // 2 - 25
                ball.rect.y = HEIGHT // 2 - 25
                ball.disabled = True
                ball.wait = 30
                score_player_1 = 0
                score_player_2 = 0
                text_score_1 = font_interface.render(str(score_player_1), True, (8, 8, 0))
                text_score_2 = font_interface.render(str(score_player_2), True, (0, 0, 0))
                finish = False

        if e.type == VIDEORESIZE:
            new_width = e.w
            new_height = int(new_width / ASPECT_RATIO)
            window = display.set_mode((new_width, new_height), RESIZABLE)
            current_size = window.get_size()

    if not finish:
        virtual_surface.fill((240, 238, 188))

        ball.update()
        ball.reset()

        player_1.update()
        player_1.reset()

        player_2.update()
        player_2.reset()

        virtual_surface.blit(text_score_1, (WIDTH // 2 - 140, 50))
        virtual_surface.blit(text_score_2, (WIDTH // 2 + 100, 50))

        if score_player_1 == 10:
            virtual_surface.blit(win_1, (WIDTH // 5, HEIGHT // 3 + 50))
            finish = True

        if score_player_2 == 10:
            virtual_surface.blit(win_2, (WIDTH // 5, HEIGHT // 3 + 50))
            finish = True

    scaled_surface = transform.scale(virtual_surface, current_size)
    window.blit(scaled_surface, (0, 0))
    clock.tick(60)
    display.update()