import pygame as pg
import random
import os, sys

pg.init()

clock = pg.time.Clock()
screen_width, screen_height = 1000, 500

# CONSTANTS

SCREEN = pg.display.set_mode((screen_width, screen_height))
RUNNING = [pg.image.load(os.path.join('textures','walk1.png')), pg.image.load(os.path.join('textures','walk2.png'))]
JUMPING = pg.image.load(os.path.join('textures','jumping.png'))
BG = pg.image.load(os.path.join('textures','background.png')).convert()
CLOUDS = [pg.image.load(os.path.join('textures','clouds.jpg')), pg.image.load(os.path.join('textures','clouds2.jpg'))]
ICON = pg.image.load(os.path.join('textures','icon.png'))
DUCKING = [pg.image.load(os.path.join('textures','ducking1.png')),pg.image.load(os.path.join('textures','ducking2.png'))]
OBSTACLES = [pg.image.load(os.path.join('textures','ob1.png')).convert(), pg.image.load(os.path.join('textures','ob2.png')).convert()]
MOUNTAINS = pg.image.load(os.path.join('textures','mountainranges.jpg'))

pg.display.set_caption("A travel back to the Mesozoic era")
pg.display.set_icon(ICON)

def load(PATH):
    with open(f'{PATH}', 'r') as file:
        data = file.read().split('\n')
        return data

class Piasaur:
    POS_X = 10
    POS_Y = 340
    JUMP_VEL = 8.79

    def __init__(self):
        self.jump_img = JUMPING
        self.run_img = RUNNING
        self.duck_img = DUCKING

        self.is_ducking = False
        self.is_jumping = False
        self.is_running = True

        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.jump_vel = self.JUMP_VEL
        self.dino_rect.x = self.POS_X
        self.dino_rect.y = self.POS_Y

    def update(self, userInput):
        if self.is_ducking:
            self.duck()
        if self.is_running:
            self.run()
        if self.is_jumping:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pg.K_UP] and not self.is_jumping: # JUMPING
            self.is_ducking = False
            self.is_jumping = True
            self.is_running = False
        elif userInput[pg.K_DOWN] and not self.is_jumping: # DUCKING
            self.is_ducking = True
            self.is_jumping = False
            self.is_running = False
        elif not(self.is_jumping or userInput[pg.K_DOWN]): # NEITHER
            self.is_ducking = False
            self.is_jumping = False
            self.is_running = True

    def duck(self):
        self.image = self.duck_img[self.step_index // 5].convert()
        self.image.set_colorkey((255,255,255))
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.POS_X
        self.dino_rect.y = self.POS_Y
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5].convert()
        self.image.set_colorkey((255,255,255))
        self.dino_rect.x = self.POS_X
        self.dino_rect.y = self.POS_Y
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img.convert()
        self.image.set_colorkey((255,255,255))
        if self.is_jumping:
            self.dino_rect.y -= round(self.jump_vel * 4)
            self.jump_vel -= 0.8

        if self.dino_rect.y >= 340:
            self.is_jumping = False
            self.dino_rect.y = self.POS_Y
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image_list = CLOUDS
        self.image = self.image_list[random.randint(0,1)]
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -(screen_width-300):
            self.x = screen_width + random.randint(200,500)

    def draw(self, SCREEN):
        try:
            SCREEN.blit(self.image, (int(self.x), int(self.y)))
        except:
            pass

class Obstacles:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width 

    def update(self):
        self.rect.x -= round(game_speed)
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def draw(self, SCREEN):
        image = self.image[self.type]
        image.set_colorkey((255,255,255))
        SCREEN.blit(image, self.rect)

class SmallF(Obstacles):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 380
    
class LargeF(Obstacles):
    def __init__(self, image):
        self.type = 1
        super().__init__(image, self.type)
        self.rect.y = 355

def game():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, hitbox, x_pos_bg2, y_pos_bg2
    obstacles = []
    points = 0
    game_speed = 8.3
    x_pos_bg, y_pos_bg = 0, 0
    x_pos_bg2, y_pos_bg2 = screen_width, 274
    font = pg.font.Font('freesansbold.ttf', 20)
    hitbox = False
    running = True
    player = Piasaur()
    cloud = Cloud()
    
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1.7

        text = font.render(f"Points: {points}", True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (300, 40)
        SCREEN.blit(text, textRect)
    
    def background():
        global x_pos_bg, y_pos_bg, x_pos_bg2, y_pos_bg2
        image_width = BG.get_width()

        SCREEN.blit(MOUNTAINS,(int(x_pos_bg2), int(y_pos_bg2)))
        
        BG.set_colorkey((255,255,255))
        SCREEN.blit(BG, (int(x_pos_bg), int(y_pos_bg)))
        SCREEN.blit(BG, (int(image_width + x_pos_bg), int(y_pos_bg)))

        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (int(image_width + x_pos_bg), int(y_pos_bg)))
            x_pos_bg = 0

        if x_pos_bg2 <= -image_width-30:
            x_pos_bg2 = 2000
        x_pos_bg -= game_speed
        x_pos_bg2 -= game_speed - 5

    while running:
        SCREEN.fill((255,255,255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    if hitbox:
                        hitbox = False
                    elif not hitbox:
                        hitbox = True

        userInput = pg.key.get_pressed()

        if len(obstacles) == 0:
            if points < 800:
                obstacles.append(SmallF(OBSTACLES))
            elif points >= 800 and points < 1600:
                if random.randint(0,50) < 30:
                    obstacles.append(SmallF(OBSTACLES))
                else:
                    obstacles.append(LargeF(OBSTACLES))
            elif points >= 1600:
                if random.randint(0,80) < 20:
                    obstacles.append(SmallF(OBSTACLES))
                else:
                    obstacles.append(LargeF(OBSTACLES))

        background()

        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(SCREEN)
            if player.dino_rect.colliderect(obstacle.rect):
                if points >= 3000:
                    credits()
                else:
                    pg.time.delay(2000)
                    death_menu()
        
        cloud.update()
        cloud.draw(SCREEN)

        player.update(userInput)
        player.draw(SCREEN)

        score()
        
        if hitbox:
            pg.draw.rect(SCREEN, (0,255,0), player.dino_rect, 2)
            if obstacles:
                pg.draw.rect(SCREEN, (255,0,0), obstacle.rect, 2)

        clock.tick(30)
        pg.display.update()

def main_menu():
    run = True
    RANGES = pg.image.load('./textures/ranges.jpg').convert()
    IMAGE = pg.image.load('./textures/yourmom.png').convert()
    MOMMY = pg.transform.scale(IMAGE, (249,327))
    LOGO = pg.image.load('./textures/piahead.jpg').convert()
    intro = -10
    size = 50
    while run:
        SCREEN.fill((255,255,255))
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                game()
                break
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if intro < 0:
            SCREEN.blit(MOMMY,(int(screen_height/2), int(screen_height/6)))
            font = pg.font.Font('freesansbold.ttf', 20)
            text = font.render(f"ΣCumpleaños / 14.1468", True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = (680, 250)
            SCREEN.blit(text, textRect)
            pg.time.delay(1000)

        if intro <= 800 and intro >= 0:
            SCREEN.blit(RANGES,(screen_height//2, screen_height//6))
            font = pg.font.Font('freesansbold.ttf', round(size))
            text = font.render(f"Powered by the Manipulato Engine", True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = (500, 120)
            SCREEN.blit(text, textRect)
            if size >= 30:
                size -= 0.1

        if intro >= 900:
            SCREEN.blit(LOGO, (360, 150))
            font = pg.font.Font('freesansbold.ttf', 20)
            text = font.render(f"Press any key to start playing! Use up key to jump and down key to squat.", True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = (500, 150)
            SCREEN.blit(text, textRect)

        if intro <= 1000:
            intro += 1
        pg.display.update()  
    pg.quit()
    sys.exit()

def death_menu():
    run = True
    LOGO = pg.image.load('./textures/piahead.jpg').convert()
    while run:
        SCREEN.fill((255,255,255))
        SCREEN.blit(LOGO, (360, 150))
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                game() 
                break
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        font = pg.font.Font('freesansbold.ttf', 20)
        text = font.render(f"OH NO, You've STUMBLED UPON F9.(PRESS ANY KEY TO RESTART) Highest point = {points}.", True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (500, 150)
        SCREEN.blit(text, textRect)
        pg.display.update()
    pg.quit()
    sys.exit()


def credits():
    credit_list = load('./docs/mono.txt')
    texts = []
    font = pg.font.SysFont("Arial", 40)
    screen_r = SCREEN.get_rect()
    for i, line in enumerate(credit_list):
        script = font.render(line, 1, (10, 10, 10))
        s_rect = script.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
        texts.append((s_rect, script))

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if e.type == pg.K_ESCAPE:
                break
        SCREEN.fill((255, 255, 255))

        for r, s in texts:
            # now we just move each rect by one pixel each frame
            r.move_ip(0, -1)
            # and drawing is as simple as this
            SCREEN.blit(s, r)

        # if all rects have left the screen, we exit
        if not screen_r.collidelistall([r for (r, _) in texts]):
            return

        # only call this once so the screen does not flicker
        pg.display.flip()

        # cap framerate at 60 FPS
        clock.tick(60)

main_menu()