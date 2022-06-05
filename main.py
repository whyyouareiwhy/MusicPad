# Yuriy Alexander
# CS410 Computers, Sound & Music
# Final Project

import simpleaudio as sa
import sounddevice as sd
from scipy.io import wavfile
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

FPS = 60
SAMPLERATE = 48000
DURATION = 1
TIMER = pygame.time.Clock()
BEATS = 8
BPM = 240
NUM_INST = 6
INSTRUMENTS = []

# Default instrument Sounds
hi_hat = mixer.Sound('sounds/tr808-hi hat.wav')
INSTRUMENTS.append(hi_hat)
snare = mixer.Sound('sounds/tr808-snare.wav')
INSTRUMENTS.append(snare)
kick = mixer.Sound('sounds/tr808-kick.wav')
INSTRUMENTS.append(kick)
cowbell = mixer.Sound('sounds/tr505-cowb-h.wav')
INSTRUMENTS.append(cowbell)
clap = mixer.Sound('sounds/tr808-clap.wav')
INSTRUMENTS.append(clap)
tom = mixer.Sound('sounds/tr505-tom-l.wav')
INSTRUMENTS.append(tom)

pygame.mixer.set_num_channels(NUM_INST * 3)  # Add more usable channels to avoid interference


# Create a list of beats/instruments that are all -1 (unclicked) then
# updated in main loop if clicked (changed to +1)
clicked = [[-1 for _ in range(BEATS)] for _ in range(NUM_INST)]

# Instruments selected by user in left instrument menu
# All are inactive for recording to start, and have default instrument selected
active_list = [1 for _ in range(NUM_INST)]


# Record audio for audio1 - audio5 to replace default instrument sound
def record(audio_num):
    audio_track = 'sounds/audio' + str(audio_num + 1) + '.wav'
    mic_input = sd.rec(frames=int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1)
    sd.wait()
    wavfile.write(audio_track, SAMPLERATE, mic_input)


# Record audio to replace instrument sound
def change_notes(inst_num):
    record(inst_num)
    if inst_num == 0:  # Instrument 1 (Hi Hat default)
        INSTRUMENTS[i] = mixer.Sound('sounds/audio1.wav')
    if inst_num == 1:  # Instrument 1 (Hi Hat default)
        INSTRUMENTS[i] = mixer.Sound('sounds/audio2.wav')
    if inst_num == 2:  # Instrument 1 (Hi Hat default)
        INSTRUMENTS[i] = mixer.Sound('sounds/audio3.wav')
    if inst_num == 3:  # Instrument 1 (Hi Hat default)
        INSTRUMENTS[i] = mixer.Sound('sounds/audio4.wav')
    if inst_num == 4:  # Instrument 1 (Hi Hat default)
        INSTRUMENTS[i] = mixer.Sound('sounds/audio5.wav')
    if inst_num == 5:  # Instrument 1 (Hi Hat default)
        INSTRUMENTS[i] = mixer.Sound('sounds/audio6.wav')


# Play default tr 808 drum samples
def play_notes(beat):
    for i in range(len(clicked)):
        if clicked[i][beat] == 1:
            if i == 0:
                INSTRUMENTS[0].play()
            if i == 1:
                INSTRUMENTS[1].play()
            if i == 2:
                INSTRUMENTS[2].play()
            if i == 3:
                INSTRUMENTS[3].play()
            if i == 4:
                INSTRUMENTS[4].play()
            if i == 5:
                INSTRUMENTS[5].play()


def draw_grid(clicks, beat, active_inst):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200], 5)
    grid_boxes = []
    colors = [gray, white, gray]

    # Draw instrument text
    if active_inst[0] == 1:
        screen.blit(label_font.render('Hi Hat', True, colors[active_inst[0]]), (30, 30))
    elif active_inst[0] == -1:
        screen.blit(label_font.render('REC 1', True, colors[active_inst[0]]), (30, 30))
    if active_inst[1] == 1:
        screen.blit(label_font.render('Snare', True, colors[active_inst[1]]), (30, 130))
    elif active_inst[1] == -1:
        screen.blit(label_font.render('REC 2', True, colors[active_inst[1]]), (30, 130))
    if active_inst[2] == 1:
        screen.blit(label_font.render('Kick', True, colors[active_inst[2]]), (30, 230))
    elif active_inst[2] == -1:
        screen.blit(label_font.render('REC 3', True, colors[active_inst[2]]), (30, 230))
    if active_inst[3] == 1:
        screen.blit(label_font.render('Cowbell', True, colors[active_inst[3]]), (30, 330))
    elif active_inst[3] == -1:
        screen.blit(label_font.render('REC 4', True, colors[active_inst[3]]), (30, 330))
    if active_inst[4] == 1:
        screen.blit(label_font.render('Clap', True, colors[active_inst[4]]), (30, 430))
    elif active_inst[4] == -1:
        screen.blit(label_font.render('REC 5', True, colors[active_inst[4]]), (30, 430))
    if active_inst[5] == 1:
        screen.blit(label_font.render('Floor Tom', True, colors[active_inst[5]]), (30, 530))
    elif active_inst[5] == -1:
        screen.blit(label_font.render('REC 6', True, colors[active_inst[5]]), (30, 530))

    # Draw borders around instrument text
    for i in range(NUM_INST):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 5)
    # Draw music pad squares
    for i in range(BEATS):
        for j in range(NUM_INST):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // BEATS) + 205, (j * 100) + 5,
                                                    ((WIDTH - 200) // BEATS) - 10,
                                                    ((HEIGHT - 200) // NUM_INST) - 10], 0, 5)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // BEATS) + 200, (j * 100), ((WIDTH - 200) // BEATS),
                                            ((HEIGHT - 200) // NUM_INST)], 5, 5)
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // BEATS) + 200, (j * 100), ((WIDTH - 200) // BEATS),
                                             ((HEIGHT - 200) // NUM_INST)], 2, 5)

            grid_boxes.append((rect, (i, j)))  # Return rectangle for each beat & coordinate for collision detection
            active_col = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // BEATS) + 200, 0,
                                                         ((WIDTH - 200) // BEATS), NUM_INST * 100], 5, 3)
    return grid_boxes


# Main game loop
# def game_loop(BPM, BEATS):
    # bpm = 240
    # beats = 8
playing = True
active_beat = 1
active_length = 0
beat_changed = True
run = True
while run:
    # bpm = BPM
    # beats = BEATS
    TIMER.tick(FPS)
    screen.fill(black)  # background

    main_boxes = draw_grid(clicked, active_beat, active_list)  # clicked tells draw_grid which boxes to turn on/off

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
    bpm_text2 = label_font.render(f'{BPM}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
    add_text = medium_font.render('+10', True, white)
    sub_text = medium_font.render('-10', True, white)
    screen.blit(add_text, (515, HEIGHT - 140))
    screen.blit(sub_text, (515, HEIGHT - 90))
    # Beats button
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (625, HEIGHT - 130))
    beats_text2 = label_font.render(f'{BEATS}', True, white)
    screen.blit(beats_text2, (670, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, white)
    sub_text2 = medium_font.render('-1', True, white)
    screen.blit(add_text2, (815, HEIGHT - 140))
    screen.blit(sub_text2, (815, HEIGHT - 90))

    # Invisible instrument rect buttons for interaction
    instrument_rects = []
    for i in range(NUM_INST):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)

    # Play instruments on each beat
    if beat_changed:
        play_notes(active_beat)
        beat_changed = False

    # Event handling for clicking music pad buttons
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
            # BPM add/sub button pressed
            elif bpm_add_rect.collidepoint(event.pos):
                BPM += 10
            elif bpm_sub_rect.collidepoint(event.pos):
                BPM -= 10
            # Beats add/sub button pressed
            elif beats_add_rect.collidepoint(event.pos):
                BEATS += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)  # Add column of inactive pads
            elif beats_sub_rect.collidepoint(event.pos):
                BEATS -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)  # Remove right-most column of pads
            ''' Instrument button pressed '''
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1  # turn on/off
                    # If original sound is turned off, new sound recorded and played instead
                    if active_list[i] == -1:
                        change_notes(i)
                    # If recording turned off, go back to original instrument sound
                    else:
                        if i == 0:
                            INSTRUMENTS[i] = mixer.Sound('sounds/tr808-hi hat.wav')
                        if i == 1:
                            INSTRUMENTS[i] = mixer.Sound('sounds/tr808-snare.wav')
                        if i == 2:
                            INSTRUMENTS[i] = mixer.Sound('sounds/tr808-kick.wav')
                        if i == 3:
                            INSTRUMENTS[i] = mixer.Sound('sounds/tr505-cowb-h.wav')
                        if i == 4:
                            INSTRUMENTS[i] = mixer.Sound('sounds/tr808-clap.wav')
                        if i == 5:
                            INSTRUMENTS[i] = mixer.Sound('sounds/tr505-tom-l.wav')

    beat_length = (FPS * 60) // BPM
    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < (BEATS - 1):
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


# if __name__ == '__main__':
#     game_loop(BPM, BEATS)
