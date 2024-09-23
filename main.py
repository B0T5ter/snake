import pygame
import random
pygame.font.init()
pygame.mixer.init()

windowHeight, windowWidth = 500, 500  
screen = pygame.display.set_mode((windowWidth,windowHeight))
CLOCK = pygame.time.Clock()
czasRuchu = 20

ost = pygame.mixer.Sound("ost.mp3")
collectio_sound = pygame.mixer.Sound("collection_sound.mp3")
pygame.mixer.Sound.play(ost)
class Segment:
    def __init__(self, x, y, numer, timer = czasRuchu) -> None:
        self.x = x
        self.y = y
        self.numer = numer
        self.timer = timer
        self.pozostalo = timer

    def ruch(self, x):
        self.pozostalo -= 1
        if self.pozostalo == 0:
            if self.numer == 1:
                self.x = glowa.x
                self.y = glowa.y
            else:
                self.x = segmenty[x - 1].x
                self.y = segmenty[x - 1].y
            self.pozostalo = self.timer
        
    def draw(self):
        pygame.draw.rect(screen, (0, 255,100), pygame.Rect(self.x, self.y, 50, 50))

class Glowa:
    def __init__(self, x = 250, y = 250, kierunek = 1, timer = czasRuchu) -> None:
        self.x = x
        self.y = y
        self.kierunek = kierunek
        self.timer = timer
        self.pozostalo = timer
    def ruch(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d] == True and self.kierunek != 3:
            self.kierunek = 1
        if key[pygame.K_w] == True and self.kierunek != 4:
            self.kierunek = 2
        if key[pygame.K_a] == True and self.kierunek != 1:
            self.kierunek = 3
        if key[pygame.K_s] == True and self.kierunek != 2:
            self.kierunek = 4
        self.pozostalo -= 1
        if self.pozostalo == 0:
            if self.kierunek == 1:
                self.x += 50
            if self.kierunek == 2:
                self.y -= 50
            if self.kierunek == 3:
                self.x -= 50
            if self.kierunek == 4:
                self.y += 50
            self.pozostalo = self.timer

    def zebranie_jagody(self):
        global score
        if self.x == jagoda.x and self.y == jagoda.y:
            jagoda.losowanie()
            segmenty.append(Segment(segmenty[len(segmenty) - 1].x, segmenty[len(segmenty) - 1].y, segmenty[len(segmenty) - 1].numer + 1))
            score += 1
            pygame.mixer.Sound.play(collectio_sound)

    def draw(self):
        pygame.draw.rect(screen, (0, 255,0), pygame.Rect(self.x, self.y, 50, 50))

        
class Jagoda:

    def __init__(self) -> None:
        self.losowanie()
    
    def losowanie(self):
        while True:
            self.x = random.randint(0,9) * 50
            self.y = random.randint(0,9) * 50
            czy_git = True
            if glowa.x == self.x and glowa.y == self.y:
                continue
            for segment in segmenty:
                if segment.x == self.x and self.y == segment.y:
                    czy_git == False
                    break
            if czy_git == True:
                break

    def draw(self):
        pygame.draw.rect(screen, (255, 0,0), pygame.Rect(self.x, self.y, 50, 50))

segmenty = [Segment(200,250,1), Segment(150,250,2), Segment(100,250,2)]
glowa = Glowa()
jagoda = Jagoda()
global score
score = 0
font = pygame.font.Font('JacquardaBastarda9-Regular.ttf', 48)
czy_gra = True

while czy_gra:
    screen.fill('black')
  
    jagoda.draw()
    glowa.zebranie_jagody()
    #print(jagoda.x, jagoda.y)
    for x in range(len(segmenty)-1,-1, -1):
        segmenty[x].ruch(x)
        segmenty[x].draw()
    glowa.ruch()
    glowa.draw()    

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    for segment in segmenty:
            if glowa.x == segment.x and glowa.y == segment.y:
                czy_gra = False
                print(czy_gra)
    if glowa.x >= 500 or glowa.x < 0 or glowa.y >= 500 or glowa.y < 0:
        czy_gra = False
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()
    CLOCK.tick(60)

while True:
    screen.fill('black')
    score_text = font.render(f'Game Over', True, (255, 255, 255))
    screen.blit(score_text, (120, 130))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (120, 180))

    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()