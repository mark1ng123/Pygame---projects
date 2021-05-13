import pygame
import os
import random
import time

# Setting up window:
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
pygame.font.init()

# Loading Images:
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers:
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# BackGround:
BG = pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))

# Globals:
LOST = False
LOST_COUNTER = 0
LEVEL = 0
LIVES = 5
WAVE_LENGTH = 5
ENEMY_VEL = 1
PLAYER_VEL = 10
LASER_VEL = 15
ENEMY_LASER_VEL = 3


class Laser:

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        # Laser hitbox:
        self.mask = pygame.mask.from_surface(img)

    # Drawing method:
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # Movement method:
    def move(self, vel):
        self.y += vel

    # Returning wheter the laser went off the screen:
    def off_screen(self, height):
        return not (height > self.y >= 0)

    # Collision method using collide function:
    def collison(self, obj):
        return collide(self, obj)


# Main ship class
class Ship:
    # Shooting cooldown class global
    COOLDOWN = 10

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    # Drawing method
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(WIN)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collison(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    # Anti spam:
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # Hitbox:
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collison(obj):
                        obj.health -= 10
                        if obj.health == 0:
                            objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                         self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                         self.ship_img.get_width() * (1 - ((self.max_health - self.health) / self.max_health)), 10))


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),

    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        if color == "red":
            self.ship_img, self.laser_img = self.COLOR_MAP[color]
            self.health = 30
        elif color == "green":
            self.ship_img, self.laser_img = self.COLOR_MAP[color]
            self.health = 20
        elif color == "blue":
            self.ship_img, self.laser_img = self.COLOR_MAP[color]
            self.health = 10

        # Enemy hitbox:
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


# Collide function:
def collide(obj1, obj2):
    # Checking wheter the laser hit the ship, using offset calculated with the x's and y's of the objects:
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


# Main:
def main():
    # Calling globals
    global LOST
    global LOST_COUNTER
    global LEVEL
    global LIVES
    global WAVE_LENGTH
    global ENEMY_VEL
    global PLAYER_VEL
    global LASER_VEL
    global ENEMY_LASER_VEL

    LOST = False
    run = True
    LEVEL = 0
    LIVES = 5
    FPS = 60
    clock = pygame.time.Clock()

    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    enemies = []

    Ship = Player(WIDTH // 2 - 50, 630)

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # Draw text:
        lives_label = main_font.render(f"Lives: {LIVES}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {LEVEL}", True, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        Ship.draw(WIN)

        # Losing labels:
        if Ship.health == 0:
            lost_label = lost_font.render("You Lost 1 life!", True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))
        elif LOST:
            lost_label = lost_font.render("You Lost!", True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        for enemy in enemies:
            enemy.draw(WIN)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        # Check if lost:
        if LIVES <= 0:
            LOST = True
            LOST_COUNTER += 1

        elif Ship.health <= 0:
            LIVES -= 1
            Ship.health = 100
            pygame.time.delay(3000)

        # Show message and break loop:
        if LOST:
            if LOST_COUNTER > FPS * 3:
                run = False
            else:
                continue

        # Creating enemies or Advancing in the game:
        if len(enemies) == 0:
            # Making it harder each level:
            LEVEL += 1
            WAVE_LENGTH += 5
            ENEMY_VEL += 1
            ENEMY_LASER_VEL += 1
            # Drawing enemy above the screen:
            for i in range(WAVE_LENGTH):
                enemy = Enemy(random.randrange(100, WIDTH - 100), random.randrange(-1500 * LEVEL // 2, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
        # Cheking if player quits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        KEYS = pygame.key.get_pressed()
        if KEYS[pygame.K_a] and Ship.x - PLAYER_VEL > PLAYER_VEL:  # left
            Ship.x -= PLAYER_VEL
        if KEYS[pygame.K_d] and Ship.x + PLAYER_VEL + Ship.get_width() < WIDTH:  # right
            Ship.x += PLAYER_VEL
        if KEYS[pygame.K_w] and Ship.y - PLAYER_VEL > PLAYER_VEL:  # up
            Ship.y -= PLAYER_VEL
        if KEYS[pygame.K_s] and Ship.y + PLAYER_VEL + Ship.get_height() + 15 < HEIGHT:  # down
            Ship.y += PLAYER_VEL
        if KEYS[pygame.K_SPACE]:
            Ship.shoot()

        # Enemy downward movement:
        for enemy in enemies[:]:

            enemy.move(ENEMY_VEL)
            # Laser randomize shooting:
            enemy.move_lasers(ENEMY_LASER_VEL, Ship)
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, Ship):
                Ship.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                Ship.health -= 10
                enemies.remove(enemy)

        # Fixing shooting upwards:
        Ship.move_lasers(-LASER_VEL, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press Right-Click to begin!", True, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


if __name__ == '__main__':
    main_menu()
