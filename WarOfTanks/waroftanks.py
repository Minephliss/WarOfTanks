#================Import Module
import pygame
import sys, os
import math
import random


#================Define Class
class Tank(pygame.sprite.Sprite):
    """This class is the tank that players controled."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_image('tank.png').convert(), (30, 30))
        self.rect = self.image.get_rect()
        self.speed = 5
    
    def update(self):
        """This function update the tank's state."""
        target_pos = pygame.mouse.get_pos()
        dis = self.move(target_pos)
        self.rect.centerx += dis[0]
        self.rect.centery += dis[1]

    def get_pos(self):
        """Return the tank's current position"""

        return (self.rect.centerx, self.rect.centery)

    def __sin__(self, x, y):
        """Return the sine."""

        return min(y / math.sqrt(x ** 2 + y ** 2), 1.0)

    def __cos__(self, x, y):
        """Return the cosine."""

        return min(x / math.sqrt(x ** 2 + y ** 2), 1.0)

    def __equal__(self, target_pos):
        """Judge the equality between two position"""

        pos = (self.rect.centerx, self.rect.centery)
        return distance(pos, target_pos) <= self.speed / 2

    def move(self, targetpos):
        """This function leads the tank to the target position."""

        delta_x = targetpos[0] - self.rect.centerx
        delta_y = targetpos[1] - self.rect.centery
        if self.__equal__(targetpos):
            return (0, 0)
        else:
            return (self.speed * self.__cos__(delta_x, delta_y), self.speed * self.__sin__(delta_x, delta_y))


class Bullet(pygame.sprite.Sprite):
    """This class is the bullet.""" 

    def __init__(self, pos, target, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_image(name).convert(), (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 10
        self.shooted = False
        self.deltax = self.speed * self.__cos__(target[0] - self.rect.centerx, target[1] - self.rect.centery)
        self.deltay = self.speed * self.__sin__(target[0] - self.rect.centerx, target[1] - self.rect.centery)

    def __sin__(self, x, y):
        """Return the sine."""

        return min(y / math.sqrt(x ** 2 + y ** 2), 1.0)

    def __cos__(self, x, y):
        """Return the cosine."""

        return min(x / math.sqrt(x ** 2 + y ** 2), 1.0)

    def move(self):
        """The bullet's route"""

        return (self.rect.centerx + self.deltax, self.rect.centery + self.deltay)

    def update(self):
        if self.shooted:
            self.kill()
        else:
            self.rect.center = self.move()
    
    def __shooted(self):
        self.shooted = True


class Enemy(pygame.sprite.Sprite):
    """This class is the enemy tank."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_image('enemy.png').convert(), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = random_pos((self.rect.width,self.rect.height))
        self.shooted = False

    def __shooted(self):
        self.shooted = True

    def update(self):
        if self.shooted:
            self.kill()
          
class Score(pygame.sprite.Sprite):
    global score
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        font = pygame.font.Font(None, 36)
        self.image = font.render('Score: {}'.format(score), 1, (10, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 10, 10
    
    def update(self):
        font = pygame.font.Font(None, 36)
        self.image = font.render('Score: {}'.format(score), 1, (10, 10, 10))


#================Define Function
def load_image(name):
    """This function will load the image of the object."""

    mainpath = os.path.split(os.path.abspath(__file__))[0]
    datapath = os.path.join(mainpath, 'data')
    filepath = os.path.join(datapath, name)
    return pygame.image.load(filepath).convert()


def load_sound(name):
    """This function will load the sound."""

    mainpath = os.path.split(os.path.abspath(__file__))[0]
    datapath = os.path.join(mainpath, 'data')
    filepath = os.path.join(datapath, name)
    return pygame.mixer.Sound(filepath)

def distance(pos1, pos2):
    """Get the distance between two positions."""

    deltax = pos1[0] - pos2[0]
    deltay = pos1[1] - pos2[1]
    return math.sqrt(deltax ** 2 + deltay ** 2)

def random_pos(object_size):
    """Return a random position"""

    screen = pygame.display.get_surface()
    x = random.random() * 10000 % (screen.get_rect().width - object_size[0])
    y = random.random() * 10000 % (screen.get_rect().height - object_size[1])
    return (x, y)

def main():
    """This is the main function."""
    global score
    version = 'v0.1'

    pygame.init()

    pygame.display.set_caption('War Of Tanks ' + version)
    score = 0

    screen = pygame.display.set_mode((1000, 500))
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255, 255, 255))

    fire = load_sound('fire.wav')
    boom = load_sound('boom.wav')

    ADD_ENEMY = pygame.USEREVENT
    ENEMY_ATTACK = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_ENEMY, 4000)
    pygame.time.set_timer(ENEMY_ATTACK, 5000)

    tank = Tank()
    thescore = Score()
    allsprites = pygame.sprite.RenderPlain(thescore, tank)
    bullets = pygame.sprite.RenderPlain()
    enemygroup = pygame.sprite.RenderPlain()
    enemybullets = pygame.sprite.RenderPlain()

    clock = pygame.time.Clock()

    going = True
    while going:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                fire.play()
                bullet = Bullet(tank.get_pos(), pygame.mouse.get_pos(), 'tankbullet.png')
                bullets.add(bullet)
                allsprites.add(bullet)
            if event.type == ADD_ENEMY:
                enemy = Enemy()
                enemygroup.add(enemy)
                allsprites.add(enemy)
            if event.type == ENEMY_ATTACK and enemygroup:
                fire.play()
                for enemy in enemygroup:
                    bullet = Bullet(enemy.rect.center, tank.rect.center, 'enemybullet.png')
                    allsprites.add(bullet)
                    enemybullets.add(bullet)
        
        for bullet in pygame.sprite.groupcollide(bullets, enemygroup, 1, 1):
            boom.play()
            score += 1

        for bullet in pygame.sprite.spritecollide(tank, enemybullets, 1):
            boom.play()
            score -= 1

        allsprites.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()


#================Main Loop
if __name__ == "__main__":
    main()