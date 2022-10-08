from pygame import *
import time as vrema
from random import randint
window = display.set_mode((1000, 900))
display.set_caption("Космос")
clock = time.Clock()
paint = transform.scale(image.load("kosmos.jpg"),(1000, 900))
FPS = 60
mixer.init()
mixer.music.load('rockbaby.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, paint, width, height, player_x, bot_y, step):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(paint), (self.width, self.height))
        self.step = step
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = bot_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.step
        if self.rect.y < -self.height:
            self.kill()

bullets = sprite.Group()






class Player (GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        
        if keys_pressed[K_LEFT] and self.rect.x >= self.step:
            self.rect.x -= self.step
        
        if keys_pressed[K_RIGHT] and self.rect.x <= (1000 - self.width - self.step ):
            self.rect.x += self.step
    def fire (self):
        bullet = Bullet('bullet.png', 20, 15, (self.rect.x +10), 780, 5)
        bullets.add(bullet)
lost =0
class Enemy (GameSprite):
    def update (self):
        self.rect.y += self.step
        global lost
        if self.rect.y > 900:
            lost += 1
            self.rect.y = - 110
            self.rect.x = randint(0, 890)
        


serdce = transform.scale(image.load("serdce.png"),(10, 10))
pobeda = transform.scale(image.load("win.jpg"),(1000, 900))
proigral = transform.scale(image.load("losed.jpg"),(1000, 900))
kosmolet = Player('rocket.png',90, 110, 400, 790, 10 )
wragi = sprite.Group()
asteorid = sprite.Group()
for i in range(5):
    enemy = Enemy('wrag.png', 100, 80, randint(0, 890), - 110, randint(3,5))
    wragi.add(enemy)
    meteorit = Enemy('meteorit.jpg', 150, 100, randint(0, 890), randint(-220,-50), randint(2, 2))
    asteorid.add(meteorit)


font.init()
font2 = font.SysFont("Arial", 40)

time_of_reload = 180
gisni = 3
monsters_killed = 0
bullet_use = 0 # использвание заряда
reload_requered = False # Не обходимая перехарядка
end = False
run = True
win = True

while run:
    window.blit(paint, (0, 0))
    write_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
    write_kill = font2.render("Уничтожено: " + str(monsters_killed), 1, (255,255,255))

    write_health = font2.render("Здоровье: " + str(gisni), 1, (255, 255, 255))

    window.blit(write_lose, (20, 20))
    window.blit(write_kill, (20, 60)) # вывести надписи со счетчиками
    
    window.blit(write_health, (20, 100))
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and e.key == K_SPACE and reload_requered != True:
            fire.play()
            kosmolet.fire()
            bullet_use +=1
        elif e.type == KEYDOWN and e.key == K_q:
            bullet_use = 0
            reload_requered = False
    if lost >= 9 or monsters_killed == 20:
        end =True
    if lost >= 9 or monsters_killed == 20:
        mixer.music.stop()
        

    if not end:
        if bullet_use >= 10:
            reload_requered = True
            start_of_relating = vrema.time()
        kosmolet.reset()
        kosmolet.move()
        wragi.draw(window)
        wragi.update()
        asteorid.draw(window)
        asteorid.update()
        bullets.draw(window)
        bullets.update() 
        
        kill_list = sprite.groupcollide(wragi, bullets, True, True)
        kill_inoplantin = sprite.spritecollide(kosmolet, wragi, True)
        minus = sprite.spritecollide(kosmolet, asteorid, True)
        for wrag in kill_list:
            monsters_killed += 1
            enemy = Enemy('wrag.png', 100, 80, randint(0, 890), - 110, randint(3,5) )
            wragi.add(enemy)
        if minus:
            win = False
            end = True
        if kill_inoplantin:
            gisni -= 1
        if monsters_killed >= 20:
            end = True
        if gisni == 0 or lost >= 9:
            win = False
            end = True
    else:
        if win:# Если выигрыш, то выводится картинка победы
            window.blit(pobeda, (0, 0)) 
        else:# Если обратное тоесть проигрыш, то выводится картинка проигрыша
            window.blit(proigral,(0, 0))


    display.update()
    clock.tick(FPS)
