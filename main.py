import pygame as pg
import random
import math
import time
import sys
from os import path

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BACKGROUND = YELLOW
FPS = 200
tileSize = 64
Width = tileSize * 18
Height = tileSize * 12


class Game:

    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode((Width, Height))
        pg.display.set_caption("Wild Ocean")
        self.clock = pg.time.Clock()
        pg.key.set_repeat(1, 1)

        self.waterTile = pg.image.load('assets/waterTile.png')
        self.islandTiles = {1: pg.image.load('assets/1.png'),
                            2: pg.transform.rotate(pg.image.load('assets/1.png'), 180),
                            3: pg.transform.rotate(pg.image.load('assets/1.png'), 270),
                            4: pg.image.load('assets/4.png'),
                            5: pg.transform.rotate(pg.image.load('assets/2.png'), 270),
                            6: pg.transform.rotate(pg.image.load('assets/3.png'), 270),
                            7: pg.image.load('assets/5.png')}
        self.towerTiles = {1: pg.transform.rotate(pg.image.load('assets/tower1.png'), 270),
                           2: pg.transform.rotate(pg.image.load('assets/tower2.png'), 270)}
        self.playerShip = pg.image.load('assets/player.png')
        self.explosion = pg.image.load('assets/explosion.png')
        self.cannonBall = pg.image.load('assets/cannonBall.png')

        # music = pg.mixer.Sound('music.mp3')
        # music.set_volume(0.1)
        # pg.mixer.music.play(-1)
        self.shoot = pg.mixer.Sound('sounds/shoot.wav')
        self.shoot.set_volume(0.1)

        self.running = True
        self.map_data = []
        self.mouseX = 0
        self.mouseY = 0
        self.mouseState = 0
        # 0 -> shooting, 1 -> placing tower1, 2 -> placing tower2

    def setup(self):
        game_folder = path.dirname(__file__)
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

        for y, tiles in enumerate(self.map_data):
            for x, tile in enumerate(tiles):
                if tile == 'P':
                    player.x = x * tileSize + 32
                    player.y = y * tileSize + 32
                elif tile == '1':
                    islands.append(Island(x, y, tile))
                    Island.tileAmount += 1
                elif tile == '2':
                    islands.append(Island(x, y, tile))
                    Island.tileAmount += 1
                elif tile == '3':
                    islands.append(Island(x, y, tile))
                    Island.tileAmount += 1
                elif tile == '4':
                    islands.append(Island(x, y, tile))
                    Island.tileAmount += 1
                elif tile == '5':
                    islands.append(Island(x, y, tile))
                    Island.tileAmount += 1
                elif tile == '6':
                    islands.append(Island(x, y, tile))
                    Island.tileAmount += 1
                elif tile == '7':
                    islands.append(Island(x, y, tile))
                    Island.tileAmount += 1

        towers.append(Tower(0, tileSize * 2, 1))
        towers.append(Tower(0, tileSize * 4, 2))
        Tower.towerAmount += 2

    def update(self):
        player.update()
        for i in range(CannonBall.ballAmount):
            cannonBalls[i].update()
        for i in range(2, Tower.towerAmount):
            towers[i].update()

    def draw(self):
        self.surface.fill(BACKGROUND)

        for x in range(tileSize, Width, tileSize):
            for y in range(tileSize, Height, tileSize):
                self.surface.blit(self.waterTile, (x, y))

        for i in range(Island.tileAmount):
            islands[i].draw()

        # for x in range(0, Width, tileSize):
        #    pg.draw.line(self.surface, RED, (x, 0), (x, Height))

        # for y in range(0, Height, tileSize):
        #    pg.draw.line(self.surface, RED, (0, y), (Width, y))

        for j in range(CannonBall.ballAmount):
            cannonBalls[j].draw()

        for k in range(Tower.towerAmount):
            towers[k].draw()

        player.draw()

        pg.draw.line(self.surface, RED, (self.mouseX - 10, self.mouseY), (self.mouseX + 10, self.mouseY))
        pg.draw.line(self.surface, RED, (self.mouseX, self.mouseY - 10), (self.mouseX, self.mouseY + 10))

        pg.display.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEMOTION:
                (self.mouseX, self.mouseY) = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.mouseX >= tileSize*1.5 and self.mouseState == 0:
                    player.shoot()
                    for i in range(2, Tower.towerAmount):
                        towers[i].shoot()

                elif self.mouseX >= tileSize*1.5 and self.mouseState == 1:
                    towers.append(Tower(self.mouseX, self.mouseY, 1))
                    Tower.towerAmount += 1
                    self.mouseState = 0

                elif self.mouseX >= tileSize*1.5 and self.mouseState == 2:
                    towers.append(Tower(self.mouseX, self.mouseY, 2))
                    Tower.towerAmount += 1
                    self.mouseState = 0

                else:
                    if tileSize*2 < self.mouseY < tileSize*3 and player.money >= 20:
                        self.mouseState = 1
                        player.money -= 20
                    elif tileSize*4 < self.mouseY < tileSize*5 and player.money >= 40:
                        self.mouseState = 2
                        player.money -= 40

            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                if not player.collideTest():
                    player.x += 2 * math.sin(math.radians(player.angle))
                    player.y += 2 * math.cos(math.radians(player.angle))
            elif keys[pg.K_s]:
                player.x -= 1 * math.sin(math.radians(player.angle))
                player.y -= 1 * math.cos(math.radians(player.angle))

            if keys[pg.K_a]:
                player.angle += 2
            elif keys[pg.K_d]:
                player.angle -= 2

    def quit(self):
        self.running = False


class Player:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.health = 100
        self.money = 100
        self.image = game.playerShip
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.image = pg.transform.rotate(game.playerShip, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def collideTest(self):
        for i in range(Island.tileAmount):
            if islands[i].x < self.x < islands[i].x + tileSize and islands[i].y < self.y < islands[i].y + tileSize:
                return True
        return False

    def shoot(self):
        cannonBalls.append(CannonBall(self))
        CannonBall.ballAmount += 1
        game.shoot.play()

    def draw(self):
        pg.draw.rect(game.surface, WHITE, (6, 390, 52, 372))
        pg.draw.rect(game.surface, RED, (12, 396, 40, (player.health * 360) / 100))

        game.surface.blit(self.image, self.rect)


class Island:
    tileAmount = 0

    def __init__(self, x, y, tileType):
        self.x = x * tileSize
        self.y = y * tileSize
        self.image = game.islandTiles[int(tileType)]

    def draw(self):
        game.surface.blit(self.image, (self.x, self.y))


class CannonBall:
    ballAmount = 0

    def __init__(self, object):
        self.x = object.x
        self.y = object.y
        self.targetX = game.mouseX
        self.targetY = game.mouseY
        self.velocityX = (self.targetX - self.x) / 50
        self.velocityY = (self.targetY - self.y) / 50
        self.distance = 0
        self.isExploded = False

    def update(self):
        if not self.isExploded:
            if not self.distance == 50:
                self.x += self.velocityX
                self.y += self.velocityY
                self.distance += 1
            else:
                self.isExploded = True

    def draw(self):
        if not self.isExploded:
            game.surface.blit(game.cannonBall, (self.x-5, self.y-5))

        else:
            game.surface.blit(game.explosion, (self.x - tileSize/2, self.y - tileSize/2))


class Tower:
    towerAmount = 0

    def __init__(self, x, y, tileType):
        self.x = int(x/tileSize)*tileSize + 32
        self.y = int(y/tileSize)*tileSize + 32
        self.angle = 0
        self.tileType = tileType
        self.image = game.towerTiles[tileType]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.angle = math.degrees(math.atan((-self.y + game.mouseY) / (-game.mouseX + self.x + 0.0001))) + 180
        self.image = pg.transform.rotate(game.towerTiles[self.tileType], self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        game.surface.blit(self.image, self.rect)

    def shoot(self):
        # for i in range(self.tileType):
            cannonBalls.append(CannonBall(self))
            CannonBall.ballAmount += 1
            game.shoot.play()


if __name__ == "__main__":
    # SETUP
    game = Game()
    player = Player()
    islands = []
    cannonBalls = []
    enemies = []
    towers = []
    game.setup()

    # GAME LOOP
    while game.running:

        game.clock.tick(FPS)
        game.events()

        game.update()

        game.draw()

    pg.quit()
