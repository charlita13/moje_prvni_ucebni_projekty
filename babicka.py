import pygame
import random
import time

#tchyne je 75*75
#vnoucata 60*60

pygame.init()

#platno a obecne nastaveni
osa_x = 1200
osa_y = 750
screen = pygame.display.set_mode((osa_x, osa_y))
pygame.display.set_caption("Babicka")
hodiny = pygame.time.Clock()
fps = 60
golden = (255, 255, 204)
red = (200, 0, 0)


# ************** GAME PREP **************
class Game:
    def __init__(self, our_player, enemies):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.time_cycle = 0

        self.our_player = our_player
        self.enemies = enemies

        self.font_bold_40 = pygame.font.SysFont("georgia", 40, True)
        self.font_20 = pygame.font.SysFont("georgia", 20, True)

        #obrazky vnoucat
        # 0 = Franta, 1 = Lada, 2 = Marta, 3 = Sara, 4 = Ester, 5 = Tim, 6 - noemi, 7 = Matous
        franta = pygame.image.load("fotky/frantisek.png")
        lada = pygame.image.load("fotky/lada.jpg")
        marta = pygame.image.load("fotky/marta.jpg")
        sara = pygame.image.load("fotky/sara.png")
        ester = pygame.image.load("fotky/ester.png")
        tim = pygame.image.load("fotky/tim.jpg")
        noemi = pygame.image.load("fotky/noemi.jpg")
        matous = pygame.image.load("fotky/matous.jpg")

        self.vnoucata_obrazky = [franta, lada, marta, sara, ester, tim, noemi, matous]

        #generujeme vnouce k chyceni
        self.vnouce_co_chytam_type = random.randint(0, len(self.vnoucata_obrazky) - 1)
        self.vnouce_co_chytam_obrazek = self.vnoucata_obrazky[self.vnouce_co_chytam_type]
        self.vnouce_co_chytam_obrazek_rect = self.vnouce_co_chytam_obrazek.get_rect()
        self.vnouce_co_chytam_obrazek_rect.centerx = osa_x // 2 + 70
        self.vnouce_co_chytam_obrazek_rect.centery = 37

        #zvuky vnoucat, cesta ke zvuku
        self.vnoucata_zvuky = ["zvuky/frantisek.mp3", "zvuky/lada.mp3", "zvuky/marta.mp3", "zvuky/sara.mp3", "zvuky/ester.mp3", "zvuky/tim.mp3", "zvuky/noemi.mp3", "zvuky/matous.mp3"]

    # Kód, který je volán stále dokola
    def update(self):
        self.time_cycle += 1
        if self.time_cycle == fps:
            self.round_time += 1
            self.time_cycle = 0

        #kontrola kolize
        self.check_collisions()

    # Vykresluje vše ve hře - texty, hledané vnouce
    def draw(self):

        # Nastavení textů
        catch_text = self.font_20.render("Chyť toto vnouče", True, golden)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = osa_x // 2 - 60
        catch_text_rect.top = 27

        score_text = self.font_20.render(f"Skóre: {self.score}", True, golden)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, 3)

        lives_text = self.font_20.render(f"Životy: {self.our_player.lives}", True, golden)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (10, 27)

        round_text = self.font_20.render(f"Kolo: {self.round_number}", True, golden)
        round_text_rect = round_text.get_rect()
        round_text_rect.topright = (osa_x - 10, 11)

        time_text = self.font_20.render(f"Čas kola: {self.round_time}", True, golden)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (osa_x - 10, 42)

        # Počet, kolikrát se může Harry vrátit do bezpečné zóny
        back_safe_zone_text = self.font_20.render(f"Skok do bezpečí: {self.our_player.enter_safe_zone}", True,
                                                      golden)
        back_safe_zone_text_rect = back_safe_zone_text.get_rect()
        back_safe_zone_text_rect.topleft = (10, 51)

        # Vykreslení (blitting) do obrazovky
        screen.blit(catch_text, catch_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(lives_text, lives_text_rect)
        screen.blit(round_text, round_text_rect)
        screen.blit(time_text, time_text_rect)
        screen.blit(back_safe_zone_text, back_safe_zone_text_rect)

        # Obrázek vnoučete, které má chytit a rámeček kolem něj
        screen.blit(self.vnouce_co_chytam_obrazek, self.vnouce_co_chytam_obrazek_rect)

        # Tvary
        # Rámeček herní plochy pro vnoučata - kde se mohou vnoučata pohybovat
        pygame.draw.rect(screen, golden, (0, 75, osa_x, osa_y - 150), width=1)

    # Kontroluje kolizi tchyne a vnoučete
    def check_collisions(self):
        #ktere vnouce jsme chytili
        chycene_vnouce = pygame.sprite.spritecollideany(self.our_player, self.enemies)

        if chycene_vnouce:
            #chytili jsme spravne vnouce?
            if chycene_vnouce.type == self.vnouce_co_chytam_type:
                self.score += 1 * self.round_number

                pozdrav = pygame.mixer.Sound(self.vnoucata_zvuky[self.vnouce_co_chytam_type])
                pozdrav.play()

                #odebrani chyceneho vnoucete
                chycene_vnouce.remove(self.enemies)
                #jsou jeste dalsi vnoucata?
                if self.enemies:
                    self.choose_new_target()
                else:
                    #konec kola - vsichni chyceni
                    time.sleep(0.5)
                    self.our_player.reset()
                    self.start_new_round()
            else:
                self.our_player.lives -= 1
                self.our_player.wrong_sound.play()
                if self.our_player.lives <= 0:
                    self.pause_game(f"Dosažené skóre: {self.score}", "Pro další hru stiskni ENTER")
                    self.reset_game()
                self.our_player.reset()
                time.sleep(0.4)

    # Zahájí nové kolo - s větším počtem vnoučat v herní ploše
    def start_new_round(self):
        self.score += int(100 * (self.round_number / (1 + self.round_time)))
        self.round_time = 0
        self.time_cycle = 0
        self.round_number += 1
        self.our_player.enter_safe_zone += 1

        #skupinu vnoucat vycistime at ji muzeme nachystat na dalsi kolo
        for deleted_vnouce in group_of_grandchilds:
            self.enemies.remove(deleted_vnouce)

        for i in range(self.round_number):
            rand_value = random.randint(0, len(self.vnoucata_obrazky) - 1)
            self.enemies.add(Vnouce(random.randint(1, osa_x - 61), random.randint(76, osa_y - 211), self.vnoucata_obrazky[rand_value], rand_value))

        #nove vnouce k chyceni
        self.choose_new_target()

    # Vybírá nové vnouče, které máme chytit
    def choose_new_target(self):
        new_vnouce_to_catch = random.choice(self.enemies.sprites())
        self.vnouce_co_chytam_type = new_vnouce_to_catch.type
        self.vnouce_co_chytam_obrazek = new_vnouce_to_catch.image

    # Pozastavení hry - pauza před zahájením nové hry, na začátku při spuštění
    def pause_game(self, text1_dosazene_skore, text2_nova_hra):
        global lets_play
        prestavka = True
        while prestavka == True:
            screen.fill((0, 0, 0))

            dosazene_skore_text = self.font_bold_40.render(text1_dosazene_skore, True, golden)
            dosazene_skore_text_rect = dosazene_skore_text.get_rect()
            dosazene_skore_text_rect.center = (osa_x // 2, osa_y // 3)
            screen.blit(dosazene_skore_text, dosazene_skore_text_rect)

            zacni_dasi_hru_text = self.font_20.render(text2_nova_hra, True, golden)
            zacni_dasi_hru_text_rect = zacni_dasi_hru_text.get_rect()
            zacni_dasi_hru_text_rect.center = (osa_x // 2, (osa_y // 3 * 2))
            screen.blit(zacni_dasi_hru_text, zacni_dasi_hru_text_rect)

            pygame.display.update()

            for i in pygame.event.get():
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_RETURN:
                        prestavka = False
                if i.type == pygame.QUIT:
                    prestavka = False
                    lets_play = False


    # Resetuje hru do výchozího stavu
    def reset_game(self):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.time_cycle = 0
        self.our_player.lives = 5
        self.our_player.enter_safe_zone = 0

        self.start_new_round()

class Tchyne(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottom = osa_y + 5
        self.rect.x = (osa_x // 2)

        self.lives = 5
        self.enter_safe_zone = 0
        self.speed = 10

        self.wrong_sound = pygame.mixer.Sound("zvuky/wrong.wav")
        self.wrong_sound.set_volume(0.1)

    # Kód, který je volán stále dokola
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] == True or keys[pygame.K_UP] == True) and self.rect.top > 75:
            self.rect.y -= self.speed
        if (keys[pygame.K_s] == True or keys[pygame.K_DOWN] == True) and self.rect.bottom < osa_y - 85:
            self.rect.y += self.speed
        if (keys[pygame.K_a] == True or keys[pygame.K_LEFT] == True) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_d] == True or keys[pygame.K_RIGHT] == True) and self.rect.right < osa_x:
            self.rect.x += self.speed

    # Návrat do bezpečné zóny dole v herní ploše
    def back_to_safe_zone(self):
        if self.enter_safe_zone > 0:
            self.enter_safe_zone -= 1
            self.rect.bottom = osa_y + 10
            self.rect.x = osa_x // 2

    # Vrací hráče zpět na výchozí pozici - doprostřed bezpečné zóny
    def reset(self):
        self.rect.bottom = osa_y + 10
        self.rect.x = osa_x // 2

class Vnouce(pygame.sprite.Sprite):
    def __init__(self, x, y, image, vnouce_type):
        super().__init__()

        #obrazek vnoucete a umisteni
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #typy vnoucat
        # 0 = Franta, 1 = Lada, 2 = Marta, 3 = Sara, 4 = Ester, 5 = Tim, 6 - noemi, 7 = Matous
        self.type = vnouce_type

        #nahodny pohyb vnoucete
        self.x_move = random.choice([-1, 1])
        self.y_move = random.choice([-1, 1])
        self.speed = random.randint(1, 3)

    # Kód, který je volán stále dokola
    def update(self):
        #pohyb vnoucete
        self.rect.x += self.x_move * self.speed
        self.rect.y += self.y_move * self.speed

        #odraz vnoucete o hranu herni plochy
        if self.rect.left <= 0 or self.rect.right >= osa_x:
            self.x_move = self.x_move * -1
        if self.rect.top <= 75 or self.rect.bottom >= osa_y - 75:
            self.y_move = self.y_move * -1

# ************** GAME EXECUTION **************

#testovaci vnoucata
group_of_grandchilds = pygame.sprite.Group()

#testovaci tchyne
group_of_grandma = pygame.sprite.Group()
one_grandma = Tchyne(pygame.image.load("fotky/tchyne.jpg"))
group_of_grandma.add(one_grandma)

#objekt game a hlavni cyklus
lets_play = True

moje_hra = Game(one_grandma, group_of_grandchilds)
moje_hra.pause_game("Chytej vnoučata!", "Pohyb = šipky nebo ASWD.   Skok do bezpečné zóny = mezerník.   Zahájení hry = enter.")
moje_hra.start_new_round()

while lets_play == True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            lets_play = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                one_grandma.back_to_safe_zone()

    #barva pozadi
    screen.fill((0, 0, 0))

    #update dle Game class
    moje_hra.update()
    moje_hra.draw()

    #volani skupiny vnoucat
    group_of_grandchilds.draw(screen)
    group_of_grandchilds.update()

    #volani skupiny tchyne
    group_of_grandma.draw(screen)
    group_of_grandma.update()

    pygame.display.update()
    hodiny.tick(fps)

pygame.quit()