from turtle import *
from random import randint
from time import sleep
walls = []
ghost_walls = []
class Sprite(Turtle):
    def __init__(self, shp: str, cl: str, x, y):
        super().__init__()
        self.speed(15)
        self.penup()
        self.shape(shp)
        self.color(cl)
        self.goto(x, y)

    def move_up(self):
        self.goto(self.xcor(), self.ycor() + 5)
        for wall in walls:
            if wall.is_collision(self):
                self.goto(self.xcor(), self.ycor() - 5)

    def move_down(self):
        self.goto(self.xcor(), self.ycor() - 5)
        for wall in walls:
            if wall.is_collision(self):
                self.goto(self.xcor(), self.ycor() + 5)

    def move_right(self):
        self.goto(self.xcor() + 5, self.ycor())
        for wall in walls:
            if wall.is_collision(self):
                self.goto(self.xcor() - 5, self.ycor())

    def move_left(self):
        self.goto(self.xcor() - 5, self.ycor())
        for wall in walls:
            if wall.is_collision(self):
                self.goto(self.xcor() + 5, self.ycor())

    def is_collide(self, player):
        dist = self.distance(player.xcor(), player.ycor())
        if dist < 10:
            return True
        else:
            return False


class Wall(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.penup()
        self.speed(20)
        self.goto(x, y)
        self.shape('square')
        self.color('black')
        self.goto(x, y)
        self.width = 40
        self.height = 40

    def is_collision(self, other):
         if (self.xcor() + self.width / 2) > other.xcor() - 5 and \
                 (self.xcor() - self.width / 2) < other.xcor() + 5 and \
                 (self.ycor() + self.height / 2) > other.ycor() - 5 and \
                 (self.ycor() - self.height / 2) < other.ycor() + 5:
             return True
         else:
             return False

class Enemy(Sprite):
    def __init__(self, shp: str, cl: str, x, y):
        Sprite.__init__(self, shp, cl, x, y)
        self.penup()
        self.shape(shp)
        self.color(cl)
        self.pensize(5)
        self.goto(x,y)
        self.speed(10)
        self.step = 10

    def make_step(self):
        self.fd(self.step)
        if self.distance(self.x_end, self.y_end) < self.step:
            self.move_enemy(self.x_end, self.y_end, self.x_start, self.y_start)

    def move_enemy(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.goto(x_start, y_start)
        self.setheading(self.towards(x_end, y_end))


class Portal1(Sprite):
    def __init__(self, shp: str, cl: str, x, y):
        Sprite.__init__(self, shp, cl, x, y)
        self.shape(shp)
        self.color(cl)
        self.goto(x,y)

    def teleport1(self):
        self.goto(-100, 2)


class Portal2(Sprite):
    def __init__(self, shp: str, cl: str, x, y):
        Sprite.__init__(self, shp, cl, x, y)
        self.shape(shp)
        self.color(cl)
        self.goto(x,y)

    def teleport2(self):
        self.goto(110, 90)

def maze():
    ghost_maze()
    for i in range(-40, 70, 10):
        walls.append(Wall(-40, i))
    for i in range(-40, 40, 10):
        walls.append(Wall(40, i))
    for i in range(-120, 120, 10):
        walls.append(Wall(-180, i))
        walls.append(Wall(140, i))
    for i in range(120, 180, 10):
        walls.append(Wall(-70, i))
        walls.append(Wall(0, i))

    for i in range(-80, 50, 10):
        walls.append(Wall(i, 40))
    for i in range(-40,-10,10):
        walls.append(Wall(i, -40))
    for i in range(40,80, 10):
        walls.append(Wall(i, 0))
    for i in range(-180,-100,10):
        walls.append(Wall(i, -40))
    for i in range(-180,150,10):
        walls.append(Wall(i, -120))
    for i in range(-180,-70,10):
        walls.append(Wall(i, 120))
    for i in range(0,150,10):
        walls.append(Wall(i, 120))
    for i in range(-70,10,10):
        walls.append(Wall(i, 180))

def ghost_maze():
    for i in range(-120, -40, 10):
        ghost_walls.append(Wall(-40, i))

hideturtle()
player = Sprite("turtle", "blue", 0, 0)
winner = Sprite("turtle", "blue", -150, -80)
win = 0
bgcolor("#FFDB58")
maze()
enemy1 = Enemy("classic", "red", -150, 90)
enemy1.move_enemy(-150, 90, 80, 90)
enemy2 = Enemy("classic", "red", 110, 100)
enemy2.move_enemy(110, 90, 110, -90)
port1 = Portal1("circle", "white", 110, 90)
port2 = Portal2("circle", "white", -100, 2)

scr = getscreen()
scr.onkey(player.move_up, "Up")
scr.onkey(player.move_down, "Down")
scr.onkey(player.move_right, "Right")
scr.onkey(player.move_left, "Left")
scr.listen()
while True:
    enemy1.make_step()
    enemy2.make_step()
    if player.is_collide(winner):
        win += 1
        break
    if player.is_collide(enemy1) or player.is_collide(enemy2):
        break
    if player.is_collide(port1):
        port1.teleport1(player)
    if player.is_collide(port2):
        port2.teleport2(player)

scr.clear()
shape("turtle")
color("blue")
if win == 1:
    bgcolor("#FFDB58")
    write("GAME WIN", font = ("", 10, "bold"))
    penup()
    goto(90,10)
else:
    bgcolor("#FF0000")
    write("GAME OVER", font = ("", 10, "bold"))
    penup()
    goto(90,10)

done()