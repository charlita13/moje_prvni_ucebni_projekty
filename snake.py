from turtle import Turtle, Screen
import time
import random

body_parts = []
score = 0
max_score = 0

# screen settig
screen = Screen()
screen.bgcolor("grey")
screen.title("Snake game")
screen.setup(width=600, height=600)
screen.tracer(False)

# hlava hada
head = Turtle("square")
head.speed(0)
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# skóre
score_sign = Turtle()
score_sign.penup()
score_sign.color("white")
score_sign.hideturtle()
score_sign.goto(0, 240)
score_sign.write(f"Aktuální skóre:  \nNejvyšší skóre: ", align="center", font=("Arial", 18))


# potrava pro hada
apple = Turtle("circle")
apple.color("red")
apple.penup()
apple.goto(random.randint(-280, 280), random.randint(-280, 280))

# funkce
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    
    if head.direction == "down":
         y = head.ycor()
         head.sety(y - 20)
    
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def move_up():
    if head.direction != "down":
        head.direction = "up"

def move_down():
    if head.direction != "up":
        head.direction = "down"

def move_left():
    if head.direction != "right":
        head.direction = "left"

def move_right():
    if head.direction != "left":
        head.direction = "right"

#kliknutí na klávesy
screen.listen()
screen.onkeypress(move_up, "w")
screen.onkeypress(move_down, "s")
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")

# hlavní cyklus
while True:
    screen.update()

    # kontrola kolize s krajem obrazovky
    if head.xcor() >= 300 or head.xcor() <= -300 or head.ycor() >= 300 or head.ycor() <= -300:
        time.sleep(3)
        head.goto(0, 0)
        head.direction = "stop"

        # reset skóre
        score = 0

        score_sign.clear()
        score_sign.write(f"Aktuální skóre: {score} \nNejvyšší skóre: {max_score}", align="center", font=("Arial", 18))

        # vyresetujeme tělo (pošleme mimo obrazovku)
        for i in body_parts:
            i.goto(350, 350)
        body_parts.clear()

    # kontrola kontaktu hlavy a jablka
    if head.distance(apple) < 18:
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        apple.goto(x, y)
        score += 1

        if score > max_score:
            max_score = score
        
        score_sign.clear()
        score_sign.write(f"Aktuální skóre: {score} \nNejvyšší skóre: {max_score}", align="center", font=("Arial", 18))

        # přidání části těla hada
        new_body_part = Turtle("square")
        new_body_part.color("brown")
        new_body_part.speed(0)
        new_body_part.penup()
        body_parts.append(new_body_part)

    # vykreslení těla hada
    for i in range(len(body_parts) - 1, 0, -1):
        x = body_parts[i - 1].xcor()
        y = body_parts[i - 1].ycor()
        body_parts[i].goto(x, y)

    if len(body_parts) > 0:
        x = head.xcor()
        y = head.ycor()
        body_parts[0].goto(x, y)

    move()

    #kolize hlavy a těla
    for i in body_parts:
        if i.distance(head) < 15:
            time.sleep(3)
            head.goto(0, 0)
            head.direction = "stop"

            # reset skóre
            score = 0

            score_sign.clear()
            score_sign.write(f"Aktuální skóre: {score} \nNejvyšší skóre: {max_score}", align="center", font=("Arial", 18))

        # vyresetujeme tělo (pošleme mimo obrazovku)
            for i in body_parts:
                i.goto(350, 350)
            body_parts.clear()
                
    time.sleep(0.1)

screen.exitonclick()