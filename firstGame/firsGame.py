import pygame
import random
# Basic pygame settings:
pygame.init()
win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")
# Loading images:
walkRight = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'),
             pygame.image.load('Game/R4.png'),
             pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'),
             pygame.image.load('Game/R8.png'),
             pygame.image.load('Game/R9.png')]
walkLeft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'),
            pygame.image.load('Game/L4.png'),
            pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'),
            pygame.image.load('Game/L8.png'),
            pygame.image.load('Game/L9.png')]
BG = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')
# Setting fps in main loop:
clock = pygame.time.Clock()
# Setting up background Music:
bulletSound = pygame.mixer.Sound('Game/Game_bullet.mp3')
hitSound = pygame.mixer.Sound('Game/Game_hit.mp3')

pygame.mixer.music.load('Game/music.mp3')
pygame.mixer.music.play(-1)
score = 0
hits = 0
counter = score + 1


# Player settings:
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        # Rectangle Hitbox around player:
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    # Draw method for every player
    def draw(self):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        # Moving the hitbox with the player:
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = random.randint(12, 450)
        self.y = 410
        self.walkCount = 0
        hitFont = pygame.font.SysFont('comoicsans', 100)
        text = hitFont.render('You got hit', True, (255, 0, 0))
        win.blit(text, (win.get_width()/2 - (text.get_width()/2), win.get_height()/2))
        pygame.display.update()
        index = 0
        while index < 100:
            pygame.time.delay(10)
            index += 1
            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    index = 301
                    pygame.quit()


# Bullet settings:
class Projectile(object):

    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction

    # Drawing method for the bullets:
    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    walkRight = [pygame.image.load('Game/R1E.png'), pygame.image.load('Game/R2E.png'),
                 pygame.image.load('Game/R3E.png'),
                 pygame.image.load('Game/R4E.png'),
                 pygame.image.load('Game/R5E.png'), pygame.image.load('Game/R6E.png'),
                 pygame.image.load('Game/R7E.png'),
                 pygame.image.load('Game/R8E.png'),
                 pygame.image.load('Game/R9E.png'), pygame.image.load('Game/R10E.png'),
                 pygame.image.load('Game/R11E.png')]
    walkLeft = [pygame.image.load('Game/L1E.png'), pygame.image.load('Game/L2E.png'), pygame.image.load('Game/L3E.png'),
                pygame.image.load('Game/L4E.png'),
                pygame.image.load('Game/L5E.png'), pygame.image.load('Game/L6E.png'), pygame.image.load('Game/L7E.png'),
                pygame.image.load('Game/L8E.png'),
                pygame.image.load('Game/L9E.png'), pygame.image.load('Game/L10E.png'),
                pygame.image.load('Game/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = (self.x, self.end)
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.hp = 9
        self.visible = True
        self.deathCount = 0

    def resurect(self):
        self.x = random.randint(0, 480)
        self.y = 410
        self.walkCount = 0
        self.hp = 9
        self.visible = True

    def displaydeath(self):
        self.deathCount += 1
        deathFont = pygame.font.SysFont('comoicsans', 30)
        text = deathFont.render('You killed ' + str(self.deathCount) + ' Goblins', True, (255, 0, 0))
        win.blit(text, (win.get_width() / 2 - (text.get_width() / 2), win.get_height() / 2))
        pygame.display.update()

    def draw(self):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            # HP bar:
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (9 - self.hp)), 10))
            # Same as the player:
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.hp > 0:
            self.hp -= 1
        else:
            self.visible = False


# Main drawing function
def redrawGameWindow():
    win.blit(BG, (0, 0))
    # Printing the score:
    text = font.render('SCORE: ' + str(score), True, (0, 0, 0))
    win.blit(text, (0, 10))
    goblin.draw()
    ally.draw()
    for firePower in ammo:
        firePower.draw()
    pygame.display.update()


# Creation:
font = pygame.font.SysFont('comicsans', 30, True, True)
ally = Player(300, 410, 64, 64)
goblin = Enemy(0, 410, 64, 64, 450)
shootingLoop = 0
ammo = []
# Main running loop:
run = True
while run:
    # fps:
    clock.tick(27)
    # Condition Player hitting enemy:
    if goblin.visible:
        if ally.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and ally.hitbox[1] + ally.hitbox[3] > goblin.hitbox[1]:
            if ally.hitbox[0] + ally.hitbox[2] > goblin.hitbox[0] and ally.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()
                ally.hit()
    # Fixing multiple shots works like a timer:
    if shootingLoop > 0:
        shootingLoop += 1
    if shootingLoop > 6:
        shootingLoop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Shooting:
    for bullet in ammo:
        # Condintion for bullet hit:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()
                hits += 1
                ammo.pop(ammo.index(bullet))
                if hits % 10 == 0:
                    score += 1
                    goblin.displaydeath()
                    if score == counter:
                        resTimer = 0
                        # Resurection timer
                        while resTimer < 100:
                            pygame.time.delay(10)
                            resTimer += 1
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    resTimer = 41
                                    pygame.quit()
                        goblin.resurect()
                        counter += 1
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            ammo.pop(ammo.index(bullet))

    # Checking movement and location:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootingLoop == 0:
        bulletSound.play()
        if ally.left:
            facing = -1
        elif ally.right:
            facing = 1
        else:
            facing = -1

        if len(ammo) < 3:
            ammo.append(
                Projectile(round(ally.x + ally.width // 2), (round(ally.y + ally.height // 2)), 5, (0, 0, 0), facing))
        # Fixing multiple shots at once:
        shootingLoop = 1

    if keys[pygame.K_LEFT] and ally.x > ally.vel:
        ally.x -= ally.vel
        ally.left = True
        ally.right = False
        ally.standing = False
    elif keys[pygame.K_RIGHT] and ally.x < 500 - ally.width - ally.vel:
        ally.x += ally.vel
        ally.right = True
        ally.left = False
        ally.standing = False
    else:
        ally.standing = True
        ally.walkCount = 0

    if not ally.isJump:
        if keys[pygame.K_UP]:
            ally.isJump = True
            ally.right = False
            ally.left = False
            ally.walkCount = 0
    else:
        if ally.jumpCount >= -10:
            neg = 1
            if ally.jumpCount < 0 or ally.y < ally.vel:
                neg = -1
            ally.y -= (ally.jumpCount ** 2) / 2 * neg
            ally.jumpCount -= 1
        else:
            ally.isJump = False
            ally.jumpCount = 10

    redrawGameWindow()

pygame.quit()
