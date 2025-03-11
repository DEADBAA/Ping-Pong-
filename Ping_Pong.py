from pygame import *
import random

Win_Size = (800, 500)
Win_W, Win_H = Win_Size
FPS = 60

font.init()
clock = time.Clock()

win = display.set_mode((Win_W, Win_H))
display.set_caption('Ping-Понг!')

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, image_filename):
        super().__init__()
        self.image = image.load(image_filename)
        self.image = transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def reset(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, width, height, speed, image_filename):
        super().__init__(x, y, width, height, speed, image_filename)
        self.keys = None

    def set_control(self, key_up, key_down, key_rest):
        self.keys = {
            'UP': key_up,
            'DOWN': key_down,
        }

    def update(self):
        key_pres = key.get_pressed()
        if key_pres[self.keys['UP']] and self.rect.y - self.speed >= 0:
            self.rect.y -= self.speed
        if key_pres[self.keys['DOWN']] and self.rect.y + self.speed <= Win_H - self.height:
            self.rect.y += self.speed
    

class Ping_Ball(GameSprite):
    def __init__(self, x, y, width, height, speed, image_filename):
        super().__init__(x, y, width, height, speed, image_filename)
        self.speed_x, self.speed_y = speed, speed
        self.last_angle = None
        self.hit_wall_sound = mixer.Sound("hit_wall.mp3")
        self.hit_racket_sound = mixer.Sound("hit_racket.mp3")
        
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <=0:
            self.speed_x *= -1 
            self.hit_wall_sound.play()
            global score_p2_counter
            score_p2_counter += 1
            
        if self.rect.x >= Win_W:
            self.speed_x *= -1 
            self.hit_wall_sound.play()
            global score_p1_counter
            score_p1_counter += 1  

        if self.rect.y <=0 or self.rect.y >= Win_H:
            self.speed_y *= -1 

        if sprite.spritecollide(self, players, False):
            possible_angles = [1, 2, 3]
            self.hit_racket_sound.play()

            if self.last_angle in possible_angles:
                possible_angles.remove(self.last_angle)
            new_angle = random.choice(possible_angles)

            if new_angle == 1:
                self.speed_y *= -1 
                self.speed_x *= -1 
            
            if new_angle == 2:
                self.speed_x *= -1 
            
            if new_angle == 3:
                self.speed_y *= -1 
            self.last_angle = new_angle

            global hit_counter
            hit_counter += 1

class Label():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = None

    def set_text(self, text, font_size=12, text_color=(0, 0, 0)):
        text_font = font.SysFont('Arial', font_size)
        self.image = text_font.render(text, True, text_color)

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))

    def update_hit(self):
        self.set_text('Количество отбиваний: ' + str(hit_counter), font_size=20, text_color=(255, 255, 255))
        self.draw(win)

    def update_score_p1(self):
        self.set_text("Счет : " + str(score_p1_counter), font_size=20, text_color=(255, 255, 0))
        self.draw(win)
    
    def update_score_p2(self):
        self.set_text("Счет : " + str(score_p2_counter), font_size=20, text_color=(139, 0, 255))
        self.draw(win)


background  = transform.scale(
    image.load("Grass.png"),
    (Win_W, Win_H)
    )

mixer.init()

mixer.music.load('kuznechik-z_uki.mp3')
mixer.music.play()

player_1 = Player(200, 250, 30, 100, 5, "Racket_1.png")
player_1.set_control(K_w, K_s, K_r)

player_2 = Player(600, 250, 30, 100, 5, "Racket_2.png")
player_2.set_control(K_UP, K_DOWN, K_h)

players = sprite.Group()
players.add(player_1)
players.add(player_2)

p_ball = Ping_Ball(400, 250, 20, 20, 5, "ball_.png")

point_p1_label = Label(10, 50)
point_p2_label = Label(100, 50)
hit_label = Label(10, 25)
win_1_label = Label(250, 200)
win_2_label = Label(250, 200)


score_p1_counter = 0
score_p2_counter = 0
hit_counter = 0
win_1, win_2 = False, False

def reset_game():
    global score_p1_counter
    score_p1_counter = 0
    global score_p2_counter
    score_p2_counter = 0
    global hit_counter
    hit_counter = 0

    win_1 = False
    win_2 = False

    player_1.rect.x = 200
    player_1.rect.y = 250
    
    player_2.rect.x = 600
    player_2.rect.y = 250

    p_ball.rect.x = 400
    p_ball.rect.y = 250

    players.empty()
    players.add(player_1)
    players.add(player_2)

game = True
while game:
    events = event.get()
    for e in events:
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_r:
            reset_game()

    win.blit(background, (0, 0))

    if not win_1 and not win_2:
        hit_label.update_hit()
        point_p1_label.update_score_p1()
        point_p2_label.update_score_p2()

        if score_p1_counter >= 10:
            win_1 = True

        if score_p2_counter >= 10:
            win_2 = True


    if not win_1 and not win_2:
        player_1.update()
        player_2.update()
        p_ball.update()
    
    player_1.reset(win)
    player_2.reset(win)
    p_ball.reset(win)

    if win_1:
        win_1_label.set_text("Победа", font_size=100, text_color=(255, 255, 0))
        win_1_label.draw(win)

    if win_2:
        win_2_label.set_text("Победа", font_size=100, text_color=(139, 0, 255))
        win_2_label.draw(win)
    
    display.update()
    clock.tick(FPS)
