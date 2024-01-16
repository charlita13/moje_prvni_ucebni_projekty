import pygame
import random
import time

pygame.init()

#barvy
grey = (111, 111, 111)
zlata = pygame.Color("#cdc335")
black = (0, 0, 0)

#hlavni parametry
zivoty = 3
skore = 0
fps = 60
hodiny = pygame.time.Clock()
pohyb_z = 10
pohyb_ost = 5
zrychleni_ost = 0.5

#editovatelne parametry
pohyb_ost_up = pohyb_ost
zivoty_up = zivoty
skore_up = skore

#platno
osa_x = 800
osa_y = 550
screen = pygame.display.set_mode((osa_x, osa_y))
pygame.display.set_caption("Zuzka chytá...")

#obrazky
zuzka = pygame.image.load("fotky/Zuzka.png")
zuzka_rect = zuzka.get_rect()
zuzka_rect.center = (40, osa_y // 2 + 25)
kaja = pygame.image.load("fotky/Kaja.png")
kaja_rect = kaja.get_rect()
kaja_rect.center = (osa_x + 50, random.randint(85, osa_y - 35))
ester = pygame.image.load("fotky/Ester.png")
ester_rect = ester.get_rect()
ester_rect.center = (osa_x + 50, random.randint(85, osa_y - 35))
sara = pygame.image.load("fotky/Sara.png")
sara_rect = sara.get_rect()
sara_rect.center = (osa_x + 50, random.randint(85, osa_y - 35))
franta = pygame.image.load("fotky/Frantisek.png")
franta_rect = franta.get_rect()
franta_rect.center = (osa_x + 50, random.randint(85, osa_y - 35))
kava = pygame.image.load("fotky/kava.png")
kava_rect = kava.get_rect()
kava_rect.center = (osa_x - 20, 50)

#fonty
font_30 = pygame.font.SysFont("kokila", 30)
font_40 = pygame.font.SysFont("kokila", 40)

#texty
hlavni_text = font_40.render(f"Zuzka řeší problémy...", True, zlata)
hlavni_rect = hlavni_text.get_rect()
hlavni_rect.center = (osa_x // 2, 25)
cil = font_30.render(f"cíl", True, zlata)
cil_rect = cil.get_rect()
cil_rect.center = (20, 80)

#zvuky
kaja_co_zase = pygame.mixer.Sound("zvuky/kaja.mp3")
e_ahoj_mami = pygame.mixer.Sound("zvuky/e_ahoj_mami.mp3")
e_boli_noha = pygame.mixer.Sound("zvuky/e_boli_noha.mp3")
e_curat = pygame.mixer.Sound("zvuky/e_curat.mp3")
e_ma_hlad = pygame.mixer.Sound("zvuky/e_ja_mam_hlad.mp3")
e_nechce_spat = pygame.mixer.Sound("zvuky/e_nechce_spat.mp3")
e_zizen = pygame.mixer.Sound("zvuky/e_zizen.mp3")
s_ahoj_mami = pygame.mixer.Sound("zvuky/s_ahoj_mami.mp3")
s_boli_noha = pygame.mixer.Sound("zvuky/s_boli_noha.mp3")
s_curat = pygame.mixer.Sound("zvuky/s_curat.mp3")
s_ma_hlad = pygame.mixer.Sound("zvuky/s_ja_mam_hlad.mp3")
s_unavena = pygame.mixer.Sound("zvuky/s_unavena.mp3")
s_zizen = pygame.mixer.Sound("zvuky/s_zizen.mp3")
franta_1 = pygame.mixer.Sound("zvuky/franta_1.mp3")
franta_2 = pygame.mixer.Sound("zvuky/franta_2.mp3")

#listy zvuku
ester_hlasy = [e_ahoj_mami, e_boli_noha, e_curat, e_ma_hlad, e_nechce_spat, e_zizen]
sara_hlasy = [s_ahoj_mami, s_boli_noha, s_curat, s_ma_hlad, s_unavena, s_zizen]
franta_hlasy = [franta_1, franta_2]

#pomocné funkce
#pohyb otravy
def pohyb(kdo, kdo_rect):
    screen.blit(kdo, kdo_rect)
    if kdo_rect.right > 0:
         kdo_rect.x -= pohyb_ost_up

#kolize s otravou
def kolize(kdo_rect, kdo_zvuk):
    global skore_up
    global pohyb_ost_up
    global volba
    global zrychleni_ost
    global zivoty_up
    global zivoty
    if zuzka_rect.colliderect(kdo_rect):
        pygame.mixer.Sound.play(kdo_zvuk)
        kdo_rect.center = (osa_x + 50, random.randint(85, osa_y - 35))
        skore_up += 1
        pohyb_ost_up += zrychleni_ost
        volba = random.randint(0, 2)
        kava_rect.x -= 90
        if kava_rect.x < 20:
            pause = True
            while pause == True:
                vyhra_text = font_30.render(f"Vyhráváš, dej si kafe a hoď nohy na stůl...",
                                            True, zlata)
                vyhra_rect = vyhra_text.get_rect()
                vyhra_rect.center = (osa_x // 2, osa_y // 2 - 50)
                zase = font_30.render(f"Pro pokračování stiskni libovolnou klávesu.",
                                            True, zlata)
                zase_rect = zase.get_rect()
                zase_rect.center = (osa_x // 2, osa_y // 2)
                screen.fill(grey)
                screen.blit(zase, zase_rect)
                screen.blit(vyhra_text, vyhra_rect)
                pygame.display.update()
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        pause = False
                        lets_play = False
                    if i.type == pygame.KEYDOWN:
                        kava_rect.center = (osa_x - 20, 50)
                        zivoty_up = zivoty
                        skore_up = skore
                        pohyb_ost_up = pohyb_ost
                        pause = False




#otrava neni chycen
def neni_kolize(kdo_rect):
    global zivoty_up
    global skore_up
    global volba
    global lets_play
    global pohyb_ost_up
    global pohyb_ost
    if kdo_rect.right <= 0:
        kdo_rect.center = (osa_x + 50, random.randint(85, osa_y - 35))
        zivoty_up -= 1
        volba = random.randint(0, 1)
        if zivoty_up == 0:
            pause = True
            while pause == True:
                znovu_text = font_30.render(f"Konec! Získáno bodů: {skore_up}. Pro pokračování stiskni libovolnou klávesu.", True, zlata)
                znovu_rect = znovu_text.get_rect()
                znovu_rect.center = (osa_x // 2, osa_y // 2)
                screen.fill(grey)
                screen.blit(znovu_text, znovu_rect)
                pygame.display.update()
                kava_rect.center = (osa_x - 20, 50)
                time.sleep(2)
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        pause = False
                        lets_play = False
                    if i.type == pygame.KEYDOWN:
                        zivoty_up = zivoty
                        skore_up = skore
                        pohyb_ost_up = pohyb_ost
                        pause = False

#hlavni cyklus
volba = random.randint(0, 2)
lets_play = True
while lets_play == True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            lets_play = False

    #pohyb zuzky
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] == True or keys[pygame.K_w] == True) and zuzka_rect.y > 60:
        zuzka_rect.y -= pohyb_z
    elif (keys[pygame.K_DOWN] == True or keys[pygame.K_s] == True) and zuzka_rect.bottom < osa_y - 10:
        zuzka_rect.y += pohyb_z

    hodiny.tick(fps)
    screen.fill(grey)

    if volba == 0:
        # ester
        pohyb(ester, ester_rect)
        kolize(ester_rect, ester_hlasy[random.randint(0, len(ester_hlasy) - 1)])
        neni_kolize(ester_rect)
    elif volba == 1:
        # sara
        pohyb(sara, sara_rect)
        kolize(sara_rect, sara_hlasy[random.randint(0, len(sara_hlasy) - 1)])
        neni_kolize(sara_rect)
    elif volba == 2:
        # franta
        pohyb(franta, franta_rect)
        kolize(franta_rect, franta_hlasy[random.randint(0, len(franta_hlasy) - 1)])
        neni_kolize(franta_rect)
    elif volba == 3:
        # kaja
        pohyb(kaja, kaja_rect)
        kolize(kaja_rect, kaja_co_zase)
        neni_kolize(kaja_rect)

    #texty
    skore_text = font_30.render(f"Score: {skore_up}", True, zlata)
    skore_rect = skore_text.get_rect()
    skore_rect.topleft = (10, 15)
    zivoty_text = font_30.render(f"Lives: {zivoty_up}", True, zlata)
    zivoty_rect = zivoty_text.get_rect()
    zivoty_rect.topright = (osa_x - 10, 15)

    pygame.draw.line(screen, zlata, start_pos=(0, 50), end_pos=(osa_x, 50))
    pygame.draw.line(screen, zlata, start_pos=(20, 40), end_pos=(20, 70))
    screen.blit(skore_text, skore_rect)
    screen.blit(zivoty_text, zivoty_rect)
    screen.blit(hlavni_text, hlavni_rect)
    screen.blit(cil, cil_rect)
    screen.blit(zuzka, zuzka_rect)
    screen.blit(kava, kava_rect)
    pygame.display.update()

pygame.quit()