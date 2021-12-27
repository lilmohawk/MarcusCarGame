import pygame
import os
import random

from pygame.event import Event
pygame.font.init()
pygame.mixer.init()

WIN = pygame.display.set_mode((500,500))                                                    #Window
pygame.display.set_caption("MARCUS GAME")
                                                                                         
white = (255,255,255)                                                                       #Controlling window
FPS = 60

gameFont = pygame.font.SysFont("comicsans", 20)                                                                                           
numOfPothole = []                                                                           #Game values(scores,money)
numOfCars = []

potholeHit = pygame.USEREVENT + 1
carHit = pygame.USEREVENT + 2
scoreInc = pygame.USEREVENT + 3
pygame.mixer.music.load(os.path.join("game", "background.mp3"))
carhorn = pygame.mixer.Sound(os.path.join("game", "carhorn.mp3"))

car = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('game', 'car.png')).convert_alpha() , (60, 90)), 180)             #change scale of car and rotation
purpleCar = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('game', 'purplecar.png')).convert_alpha(), (60, 90)), 180)
blueCar = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('game', 'bluecar.png')).convert_alpha(), (60, 90)), 180)
greenCar = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('game', 'greencar.png')).convert_alpha(), (60, 90)), 180)
pinkCar = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('game', 'pinkcar.png')).convert_alpha(), (60, 90)), 180)

carList = [pinkCar, greenCar, blueCar, purpleCar]

road = pygame.image.load(os.path.join('game', 'road.png')).convert_alpha()
pothole = pygame.transform.scale(pygame.image.load(os.path.join('game', 'pothole.png')).convert_alpha(),(30, 30))


def draw_window(car_rect, road_rect1, road_rect2, money, score):                            #Draws to the window(takes car_rect so we can move the car)
    WIN.fill((0,0,0))
    road2 = WIN.blit(road,(road_rect2.x, road_rect2.y))                                     #road two
    road1 = WIN.blit(road, (road_rect1.x, road_rect1.y))                                    #road one

    if road_rect1.y >= road.get_width():                                                    #repeating backscreen
        road_rect1.y = road.get_width() * -1
        pygame.event.post(pygame.event.Event(scoreInc))
    if road_rect2.y >= road.get_width():
        road_rect2.y = road.get_width() * -1
        pygame.event.post(pygame.event.Event(scoreInc))

    for i in range(len(numOfPothole)):
        WIN.blit(pothole, (numOfPothole[i].x, numOfPothole[i].y))
    
    for i in range(len(numOfCars)):
        WIN.blit(carList[i], (numOfCars[i].x, numOfCars[i].y))

    WIN.blit(car, (car_rect.x, car_rect.y))
    
    WIN.blit(gameFont.render("Money:$" + str(money), 1, white), (75,0))
    WIN.blit(gameFont.render("Score: " + str(score), 1, white), (350, 0))
    pygame.display.update()

def finalScreen(score):
    WIN.fill(white)
    finalText = gameFont.render("Better luck next time" , 1, (0,0,0))
    WIN.blit(finalText, (250 - finalText.get_width()//2, 250))
    finalScore = gameFont.render("Miles Traveled (score) " + str(score), 1, (0,0,0))
    WIN.blit(finalScore, (250 - finalScore.get_width()//2, 300))
    pygame.display.update()
    pygame.time.delay(5000)
                                                                       
def potholeHandle(car_rect, vel):                                                                #pothole collision handler
    for pot in numOfPothole:
        pot.y += vel
        if pot.colliderect(car_rect):
            numOfPothole.remove(pot)
            pygame.event.post(pygame.event.Event(potholeHit))

        elif pot.y > road.get_width() + 100:
            numOfPothole.remove(pot)

def carObjHandle(car_rect):
    carObjVel = 3                                                                                #Car collision handler
    for car in numOfCars:
        car.y += carObjVel
        if car.colliderect(car_rect):
            numOfCars.remove(car)
            pygame.event.post(pygame.event.Event(carHit))
            pygame.mixer.Sound.play(carhorn)
        
        elif car.y > road.get_width() + 100:
            numOfCars.remove(car)
        
        for car2 in numOfCars:
            if car != car2:
                if car2.x == car.x or car2.y == car.y:
                    numOfCars.remove(car2)
                                                                                            
def main():
    vel = 2
    money = 50
    score = 0
    car_rect = pygame.Rect(220, 400, 50, 80)
    road_rect1 = pygame.Rect(0, 0, 500, 500)
    road_rect2 = pygame.Rect(0, -500, 500, 500)
    carObjImg = 0
    
    clock = pygame.time.Clock()
    run = True
    pygame.mixer.music.play(-1, 0.0) 
    
    while run:
        clock.tick(FPS)                                                                     #Makes FPS 60 Hard Code
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == carHit:
                money -= 50

            if event.type == potholeHit:
                money -= 10
            if event.type == scoreInc:
                score += 1
                if score%5 == 0:
                    if vel != 8:
                        vel += 1

                money += 5
                
        road_rect1.y += vel
        road_rect2.y += vel

        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_LEFT] and car_rect.x >= 65:         #left
            car_rect.x -= vel 
        if keypressed[pygame.K_RIGHT] and car_rect.x <= 375:      #right
            car_rect.x += vel

        if len(numOfPothole) < 2:
            numOfPothole.append(pygame.Rect(random.randint(75, 375), -30, 30, 30))

        if len(numOfCars) < 4:
            carObjX = random.randrange(75, 425, 60)
            carObjY = random.randrange(-250, -100, 90)
            numOfCars.append(pygame.Rect(carObjX, carObjY, 50, 80))
                        
        if money <= 0:
            finalScreen(score)
            break

        potholeHandle(car_rect, vel)
        carObjHandle(car_rect)
        draw_window(car_rect, road_rect1, road_rect2, money, score)
    pygame.quit()

if __name__ == "__main__":
    main()