# Yuriy Alexander
# CS410 Computers, Sound & Music
# Final Project

import simpleaudio as sa
import pygame
from pygame import mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

# RGB
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("MusicPad")
label_font = pygame.font.Font("freesansbold.ttf", 32)
medium_font = pygame.font.Font("freesansbold.ttf", 22)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6

# Instrument Sounds
hi_hat = mixer.Sound('sounds/tr808-hi hat.wav')
snare = mixer.Sound('sounds/tr808-snare.wav')
kick = mixer.Sound('sounds/tr808-kick.wav')
Cowbell = mixer.Sound('sounds/tr505-cowb-h.wav')
clap = mixer.Sound('sounds/tr808-clap.wav')
tom = mixer.Sound('sounds/tr505-tom-l.wav')

pygame.mixer.set_num_channels(instruments * 3)  # Add more usable channels to avoid interference


# Create a list of beats/instruments that are all -1 (unclicked) then
# updated in main loop if clicked (changed to +1)
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]


# Play default tr 808 drum samples
def play_notes(beat):
    for i in range(len(clicked)):
        if clicked[i][beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                Cowbell.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200], 5)
    grid_boxes = []
    colors = [gray, white, gray]

    # Draw instrument text
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render('Kick', True, white)
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render('Cowbell', True, white)
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30, 430))
    floor_tom_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_tom_text, (30, 530))

    # Draw borders around instrument text
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 5)
    # Draw music pad squares
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5,
                                                    ((WIDTH - 200) // beats) - 10,
                                                    ((HEIGHT - 200) // instruments) - 10], 0, 5)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                                             ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                                             ((HEIGHT - 200) // instruments)], 2, 5)

            grid_boxes.append((rect, (i, j)))  # Return rectangle for each beat & coordinate for collision detection
            active_col = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0,
                                                         ((WIDTH - 200) // beats), instruments * 100], 5, 3)
    return grid_boxes


# Main game loop
def game_loop():
    bpm = 240
    playing = True
    active_beat = 1
    active_length = 0
    beat_changed = True
    run = True
    while run:
        timer.tick(fps)
        screen.fill(black)  # background

        main_boxes = draw_grid(clicked, active_beat)  # clicked tells draw_grid which boxes to turn on/off

        # Lower menu
        # Play/Pause button
        play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
        play_text = label_font.render('Play/Pause', True, white)
        screen.blit(play_text, (70, HEIGHT - 130))
        if playing:
            play_text_opt = medium_font.render('Playing', True, dark_gray)
        else:
            play_text_opt = medium_font.render('Paused', True, dark_gray)
        screen.blit(play_text_opt, (70, HEIGHT - 100))
        # BPM button
        bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
        bpm_text = medium_font.render('Beats Per Min', True, white)
        screen.blit(bpm_text, (325, HEIGHT - 130))
        bpm_text2 = label_font.render(f'{bpm}', True, white)
        screen.blit(bpm_text2, (370, HEIGHT - 100))
        bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
        bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
        add_text = medium_font.render('+10', True, white)
        sub_text = medium_font.render('-10', True, white)
        screen.blit(add_text, (515, HEIGHT - 140))
        screen.blit(sub_text, (515, HEIGHT - 90))

        # Instrument rect buttons for interaction
        instrument_rects = []
        for i in range(instruments):
            rect = pygame.rect.Rect((0, i * 100), (200, 100))
            instrument_rects.append(rect)

        # Play instruments on each beat
        if beat_changed:
            play_notes(active_beat)
            beat_changed = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Music pad buttons pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(main_boxes)):
                    if main_boxes[i][0].collidepoint(event.pos):
                        coords = main_boxes[i][1]
                        # Select a box by making it positive, unselect it by making it negative
                        clicked[coords[1]][coords[0]] *= -1
            # Menu buttons pressed
            if event.type == pygame.MOUSEBUTTONUP:
                # Play/Pause button
                if play_pause.collidepoint(event.pos):
                    if playing:
                        playing = False
                    elif not playing:
                        playing = True
                elif bpm_add_rect.collidepoint(event.pos):
                    bpm += 10
                elif bpm_sub_rect.collidepoint(event.pos):
                    bpm -= 10

        beat_length = (fps * 60) // bpm
        if playing:
            if active_length < beat_length:
                active_length += 1
            else:
                active_length = 0
                if active_beat < (beats - 1):
                    active_beat += 1
                    beat_changed = True
                else:
                    active_beat = 0
                    beat_changed = True

        pygame.display.flip()

    pygame.quit()


# def print_wav(file):
#     wave_obj = sa.WaveObject.from_wave_file(file)
#     play_obj = wave_obj.play()
#     play_obj.wait_done()


if __name__ == '__main__':
    game_loop()
