import pygame
from networking import Network
from Game import Game
import pickle

pygame.font.init()

Scissors = pygame.image.load('Assets/Scissors.png')
Rock = pygame.image.load('Assets/Rock.png')
Paper = pygame.image.load('Assets/Paper.png')
BackGround = pygame.image.load('Assets/Background.jpg')
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
score = [0, 0]

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        if self.text == "Scissors":
            font = pygame.font.SysFont("comicsans", 40)
            win.blit(Scissors, (self.x, self.y))
        elif self.text == "Rock":
            font = pygame.font.SysFont("comicsans", 40)
            win.blit(Rock, (self.x, self.y))
        elif self.text == "Paper":
            font = pygame.font.SysFont("comicsans", 40)
            win.blit(Paper, (self.x, self.y))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    global score
    win.blit(BackGround, (0, 0))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for Player...", True, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2 + 10, height / 2 - text.get_height() / 2 - 115))
    else:
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Your Move", True, (255, 255, 255))
        win.blit(text, (165, 300))

        text = font.render("Opponents", True, (255, 255, 255))
        win.blit(text, (430, 300))

        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Player 1: " + str(score[0]), True, (255, 255, 255))
        win.blit(text, (165, 100))

        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Player 2: " + str(score[1]), True, (255, 255, 255))
        win.blit(text, (430, 100))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, True, (0, 0, 0))
            text2 = font.render(move2, True, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, True, (255, 255, 255))
            elif game.p1Went:
                text1 = font.render("Locked In", True, (255, 255, 255))
            else:
                text1 = font.render("Waiting...", True, (255, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, True, (255, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", True, (255, 0, 0))
            else:
                text2 = font.render("Waiting...", True, (255, 0, 0))

        if p == 1:
            win.blit(text2, (180, 350))
            win.blit(text1, (440, 350))
        else:
            win.blit(text1, (180, 350))
            win.blit(text2, (440, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 100, 500, (0, 0, 0)), Button("Scissors", 275, 500, (255, 0, 0)),
        Button("Paper", 450, 500, (0, 255, 0))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", True, (255, 0, 0))
                score[player] += 1
            elif game.winner() == -1:
                text = font.render("Tie Game!", True, (255, 0, 0))
            else:
                text = font.render("You Lost...", True, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", True, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
