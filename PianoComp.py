import pygame
import random


def init_chords(chords, song, initRandom):  # accepts list, string song, bool initRandom
    if initRandom:
        for sound in range(3):
            for letter in range(12):
                if sound == 0:
                    extension = "7"
                    chords.append(num_letter(letter) + extension)
                elif sound == 1:
                    extension = "Mi7"
                    chords.append(num_letter(letter) + extension)
                elif sound == 2:
                    extension = "Ma7"
                    chords.append(num_letter(letter) + extension)

    elif not initRandom:
        if song == "New":  # if the new button was clicked
            songInfo = []
            chord = ''
            myfile = open("Saves.txt", "a")

            song = raw_input("Enter the name of the song: ")
            songInfo.append(song)

            while chord != "q":
                chord = raw_input("Enter Chord (format is C7, C-7, CM7, Db7, etc): ")
                songInfo.append(chord)

            for item in songInfo:
                myfile.write(item + "_")
            myfile.write('\n')

            myfile.close()

        else:  # if the song already exists
            myfile = open("Saves.txt", "r")
            fileInfo = []
            for line in myfile.readlines():
                fileInfo.append(line)
            for x in range(len(fileInfo)):
                fileInfo[x] = fileInfo[x].split("_")
            for mylist in fileInfo:
                if mylist[0] == song:  # check for the line in the saves file with the right song name
                    for x in range(1, len(mylist) - 2):
                        chords.append(mylist[x])

    return chords


def num_letter(x):  # for random generation
    if x == 0:
        return "A"
    elif x == 1:
        return "Bb"
    elif x == 2:
        return "B"
    elif x == 3:
        return "C"
    elif x == 4:
        return "Db"
    elif x == 5:
        return "D"
    elif x == 6:
        return "Eb"
    elif x == 7:
        return "E"
    elif x == 8:
        return "F"
    elif x == 9:
        return "Gb"
    elif x == 10:
        return "G"
    else:
        return "Ab"


def random_ind(chords, temp):
    r = random.randint(0, len(chords) - 1)
    while r == temp:
        r = random.randint(0, len(chords) - 1)
    return r


def main():
    black = [0, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]
    white = [255, 255, 255]
    grey = [176, 176, 176]
    light_grey = [200, 200, 200]

    lvl = 3
    time = 0
    r = 0
    temp = 0
    fps = 30

    chords = []

    pygame.init()

    screen = pygame.display.set_mode((600, 500))
    screen.fill(white)

    font = pygame.font.Font("freesansbold.ttf", 32)
    comp_font = pygame.font.SysFont("comicsansms", 150)
    pygame.display.set_caption("Piano Comping")

    Select_screen = True

    running = False  # game running
    home_screen = False
    pause = False

    song_reload = True

    bW = 50
    bH = 50
    bSpace = 5
    clock = pygame.time.Clock()

    while Select_screen:
        if song_reload:
            myfile = open("Saves.txt", "r")
            songList = ["Random"]
            for line in myfile.readlines():
                songList.append(line)
            for x in range(len(songList)):
                if x != 0:
                    songList[x] = songList[x].split("_")
            song_reload = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Select_screen = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if (550 > mouse[0] > 500) and (55 > mouse[1] > 5):
                    chords = init_chords(chords, song="New", initRandom=False)
                    song_reload = True
                for y in range(len(songList)):
                    if y == 0:
                        if (410 > mouse[0] > 10) and (
                                (y * 50) + (5 * (y + 1)) + 50 > mouse[1] > (y * 50) + (5 * (y + 1))):
                            chords = init_chords(chords, song="", initRandom=True)
                            Select_screen = False
                            running = True
                            home_screen = True
                            break
                    else:
                        if (410 > mouse[0] > 10) and (
                                (y * 50) + (5 * (y + 1)) + 50 > mouse[1] > (y * 50) + (5 * (y + 1))):
                            chords = init_chords(chords, song=songList[y][0], initRandom=False)
                            Select_screen = False
                            running = True
                            home_screen = True
                            break
        # drawing the new song button
        pygame.draw.rect(screen, grey, (500, 5, 50, 50))
        textSurface = font.render("+", True, black)
        screen.blit(textSurface, (512.5, 17.5))

        # drawing a list of buttons for each saved song
        for y in range(len(songList)):
            if y == 0:
                pygame.draw.rect(screen, grey, (10, (y * 50) + (5 * (y + 1)), 400, 50))
                textSurface = font.render(songList[y], True, black)
                screen.blit(textSurface, (10, (y * 50) + (5 * (y + 1))))
            else:
                pygame.draw.rect(screen, grey, (10, (y * 50) + (5 * (y + 1)), 400, 50))
                textSurface = font.render(songList[y][0], True, black)
                screen.blit(textSurface, (10, (y * 50) + (5 * (y + 1))))

        pygame.display.update()
        clock.tick(fps)

    screen.fill(white)
    pygame.display.update()
    clock.tick(fps)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    screen.fill(white)
                    home_screen = True

                if event.key == pygame.K_SPACE:
                    if home_screen == False and Select_screen == False:
                        if not pause:
                            pause = True
                        else:
                            pause = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if home_screen:
                    for x in range(5):
                        bRenderX = (bW * x) + bSpace * (x + 1)

                        for y in range(2):
                            bRenderY = (bH * y) + bSpace * (y + 1)

                            if (bRenderX + bW > mouse[0] > bRenderX) and (bRenderY + bH > mouse[1] > bRenderY):
                                lvl = (x + 1) + (y * 5)
                                home_screen = False

                    if (205 > mouse[0] > 5) and (165 > mouse[1] > 115):
                        lvl = 30
                        home_screen = False

        if home_screen:
            mouse = pygame.mouse.get_pos()
            for x in range(5):
                bRenderX = (bW * x) + bSpace * (x + 1)

                for y in range(2):
                    bRenderY = (bH * y) + bSpace * (y + 1)
                    pygame.draw.rect(screen, grey, (bRenderX, bRenderY, bW, bH))
                    textSurface = font.render(str((x + 1) + (y * 5)), True, black)
                    screen.blit(textSurface, (bRenderX + (bW / 4), bRenderY + (bH / 4)))

                    if (bRenderX + bW > mouse[0] > bRenderX) and (bRenderY + bH > mouse[1] > bRenderY):
                        pygame.draw.rect(screen, light_grey, (bRenderX, bRenderY, bW, bH))

            # for monkey button
            pygame.draw.rect(screen, grey, (5, 115, 200, 50))
            textSurface = font.render("Monkey", True, black)
            screen.blit(textSurface, (5, 115, 200, 50))

            if (205 > mouse[0] > 5) and (165 > mouse[1] > 115):
                pygame.draw.rect(screen, light_grey, (5, 115, 200, 50))

        else:
            if time % (30 * (11 - lvl)) == 0:
                r = random_ind(chords, temp)
                temp = r
                screen.fill(white)

            if not pause:
                time += 1

            chordSurface = comp_font.render(chords[r], True, black)
            screen.blit(chordSurface, (0, 0))

        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
