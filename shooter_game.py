from pygame import *
from time import sleep
from random import randint



w = 700
h = 500

window = display.set_mode((w, h))
display.set_caption("shooter game")



background = transform.scale(image.load('galaxy.jpg'), (w, h))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, image_filename, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_filename), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = 'left'
        self.image_filename = image_filename
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        # left and right
        if keys_pressed[K_LEFT] and (self.rect.x - self.speed) > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and (self.rect.x + self.speed) < (w - 70):
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost

        self.rect.y += self.speed
        if self.rect.y > h:
            if "ufo"in self.image_filename:
                lost += 1
                self.rect.y = 0
                self.rect.x = randint(0, w-70)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png', 100, 430, 60, 70, 10)
e1 = Enemy('ufo.png', randint(0, w-70), randint(-50, 50), 80, 50, 2)
e2 = Enemy('ufo.png', randint(0, w-70), randint(-50, 50), 80, 50, 2)
e3 = Enemy('ufo.png', randint(0, w-70), randint(-50, 50), 80, 50, 2)
e4 = Enemy('ufo.png', randint(0, w-70), randint(-50, 50), 80, 50, 2)
e5 = Enemy('ufo.png', randint(0, w-70), randint(-50, 50), 80, 50, 2)

# monsters Group
monsters = sprite.Group()
monsters.add(e1)
monsters.add(e2)
monsters.add(e3)
monsters.add(e4)
monsters.add(e5)

asteroid = Enemy("asteroid.png", randint (0, 200),- 30, 70, 40, 5)
monsters.add(asteroid)

# bullets Group 
bullets = sprite.Group()
game = True
FPS = 60
clock = time.Clock()
finish = False
lost = 0
score = 0
num_fire = 0
rel_time = False
max_lost = 8
goal = 8











font.init()
font1 = font.SysFont('Arial', 70)
win = font1.render('YOU WIN', True, (255, 215, 0))
lose = font1 .render('YOU LOSE', True, (180, 0, 0))

font2 = font.SysFont('Arial', 40)
text_miss = font2.render('Missed: ' + str(lost), 1, (255, 255, 255))
text_score = font2.render('score: ' + str(0), 1, (255, 255, 255))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire.play()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire.play()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

                        
                        
                
                

    # game logic
    if finish != True:
        # blit "render" images
        window.blit(background, (0, 0))
        player.reset()
        monsters.draw(window)
        #asteroid.draw(window)
        bullets.draw(window)
        text_miss = font2.render('Missed: ' + str(lost), 1, (255, 255, 255))
        text_score = font2.render('score: ' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))
        window.blit(text_miss, (10, 40)) 

        player.update()
        monsters.update()
        asteroid.update()
        bullets.update()


        if rel_time:
            if now_time - last_time < 3:
                rel_word = font2.render('reloading...', 1, (255, 0, 0))
                window.blit(rel_word, (260, 460))

        

        collides = sprite.groupcollide(monsters, bullets, True,True)
        for c in collides:
            score = score +1
            monster = Enemy("ufo.png", randint(80, 700 - 80), -40, 80, 50,randint(1,5))
            monster.add(monsters)

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))
        


    display.update()
    clock.tick(FPS)
