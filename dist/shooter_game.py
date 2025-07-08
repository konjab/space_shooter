from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
powerup_sound = mixer.Sound('item-pick-up-38258.mp3')

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_powerup = "heart.png"

font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 30)
font3 = font.Font(None, 80)

win = font3.render('YOU WIN!', True, (255, 255, 255))
lose = font3.render('YOU LOSE!', True, (180, 0, 0))

score = 0
lost = 0
goal = 25
max_lost = 5
lives = 3

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.fire_times = []
        self.cooldown = False
        self.cooldown_start = 0

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_0] and self.speed >= 0:
            self.speed += 1
        if keys[K_9] and self.speed > 1:
            self.speed -= 1
        if keys[K_RIGHTBRACKET]:
            self.speed = 10

    def fire(self):
        now = time.get_ticks()
        if self.cooldown:
            if now - self.cooldown_start >= 3000:
                self.cooldown = False
                self.fire_times = []
            else:
                return

        self.fire_times = [t for t in self.fire_times if now - t < 1000]
        if len(self.fire_times) >= 5:
            self.cooldown = True
            self.cooldown_start = now
            return

        self.fire_times.append(now)
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        fire_sound.play()
    def update_cooldown(self):
        if self.cooldown:
            now = time.get_ticks()
            if now - self.cooldown_start >= 3000:
                self.cooldown = False
                self.fire_times = []

class Player2(GameSprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.fire_times = []
        self.cooldown = False
        self.cooldown_start = 0

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_2] and self.speed >= 0:
            self.speed += 1
        if keys[K_1] and self.speed > 1:
            self.speed -= 1
        if keys[K_LEFTBRACKET]:
            self.speed = 10

    def fire(self):
        now = time.get_ticks()
        if self.cooldown:
            if now - self.cooldown_start >= 3000:
                self.cooldown = False
                self.fire_times = []
            else:
                return

        self.fire_times = [t for t in self.fire_times if now - t < 1000]
        if len(self.fire_times) >= 5:
            self.cooldown = True
            self.cooldown_start = now
            return

        self.fire_times.append(now)
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        fire_sound.play()
    def update_cooldown(self):
        if self.cooldown:
            now = time.get_ticks()
            if now - self.cooldown_start >= 3000:
                self.cooldown = False
                self.fire_times = []
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class PowerUp(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()

monsters = sprite.Group()
bullets = sprite.Group()
powerups = sprite.Group()

for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), 40, 80, 50, randint(1, 5))
    monsters.add(monster)

ship1 = Player(img_hero, 615, win_height - 100, 80, 100, 10)
ship2 = Player2(img_hero, 5, win_height - 100, 80, 100, 10)

powerup_timer = time.get_ticks()
powerup_interval = 10000

run = True
finish = False
blink = True
blink_timer = time.get_ticks()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                ship2.fire()
            if e.key == K_UP:
                ship1.fire()

    if not finish:
        window.blit(background, (0, 0))

        ship1.update()
        ship1.reset()
        ship2.update()
        ship2.reset()
        ship1.update_cooldown()
        ship2.update_cooldown()


        monsters.update()
        bullets.update()
        powerups.update()

        monsters.draw(window)
        bullets.draw(window)
        powerups.draw(window)

        
        current_time = time.get_ticks()
        if current_time - powerup_timer > powerup_interval:
            powerup_timer = current_time
            powerup = PowerUp(img_powerup, randint(50, win_width - 50), -50, 50, 50, 3)
            powerups.add(powerup)

        
        if sprite.spritecollide(ship1, powerups, True) or sprite.spritecollide(ship2, powerups, True):
            powerup_sound.play()
            lost = 0
            score += 5
            if lives < 3:
                lives += 1

        
        if sprite.spritecollide(ship1, monsters, False) or sprite.spritecollide(ship2, monsters, False):
            score -= 1

        
        collisions = sprite.groupcollide(monsters, bullets, True, True)
        for c in collisions:
            score += 1
            new_monster = Enemy(img_enemy, randint(80, win_width - 80), 40, 80, 50, randint(1, 5))
            monsters.add(new_monster)

        
        if lost >= max_lost or sprite.spritecollide(ship1, monsters, False) or sprite.spritecollide(ship2, monsters, False):
            lives -= 1
            if lives == 0:
                finish = True
                window.blit(lose, (200, 200))
            else:
                finish = False
                lost = 0
                for m in monsters:
                    m.rect.y = 0
                for b in bullets:
                    b.kill()

       
        score_text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        lost_text = font2.render("Lost: " + str(lost), 1, (255, 100, 100))
        lives_text = font2.render(f"Lives: {lives}", True, (255, 255, 0))
        speed_text1 = font1.render(f'Speed1: {ship2.speed}', True, (255, 255, 255))
        speed_text2 = font1.render(f'Speed2: {ship1.speed}', True, (255, 255, 255))

        window.blit(score_text, (10, 40))
        window.blit(lost_text, (10, 70))
        window.blit(lives_text, (10, 100))
        window.blit(speed_text1, (10, 10))
        window.blit(speed_text2, (560, 10))

        # Αναβοσβήνει cooldown
        if current_time - blink_timer > 300:
            blink = not blink
            blink_timer = current_time

        for ship in [(ship1, '1'), (ship2, '2')]:
            player, label = ship
            if player.cooldown and blink:
                seconds_left = 3 - (current_time - player.cooldown_start) // 1000
                cd_text = font1.render(f"Cooldown: {seconds_left}s", True, (255, 0, 0))
                window.blit(cd_text, (player.rect.x, player.rect.y - 20))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
        time.delay(50)

    else:
        time.delay(3000)
        finish = False
        score = 0
        lost = 0
        lives = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for p in powerups:
            p.kill()
        for i in range(5):
            monster = Enemy(img_enemy, randint(80, win_width - 80), 40, 80, 50, randint(1, 5))
            monsters.add(monster)