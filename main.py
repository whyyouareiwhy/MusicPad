# Yuriy Alexander
# CS410 Computers, Sound & Music
# Final Project
import io
import wave

import simpleaudio as sa
import sounddevice as sd
from scipy.io import wavfile
import pygame
import numpy as np
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
silver_blue = (220, 239, 239)

roland_red = (245, 63, 7)
roland_yellow = (242, 240, 167)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("MusicPad")
label_font = pygame.font.Font("freesansbold.ttf", 32)
label_font2 = pygame.font.Font("freesansbold.ttf", 28)
medium_font = pygame.font.Font("freesansbold.ttf", 22)

FPS = 60
SAMPLERATE = 48000
DURATION = 1
TIMER = pygame.time.Clock()
BEATS = 8
BPM = 240
NUM_INST = 6

INSTRUMENTS = []
# Default instrument files and names
INST_DEF1 = 'sounds/tr808-hi hat.wav'
INST_DEF2 = 'sounds/tr808-snare.wav'
INST_DEF3 = 'sounds/tr808-kick.wav'
INST_DEF4 = 'sounds/tr505-cowb-h.wav'
INST_DEF5 = 'sounds/tr808-clap.wav'
INST_DEF6 = 'sounds/tr505-conga-h.wav'
INST_DEF1_NAME = 'Hi Hat'
INST_DEF2_NAME = 'Snare'
INST_DEF3_NAME = 'Kick'
INST_DEF4_NAME = 'Cowbell'
INST_DEF5_NAME = 'Clap'
INST_DEF6_NAME = 'Conga'

# Default instrument recording file names to be used if necessary
INST1_REC = 'audio1.wav'

REC1 = False  # Recording for instrument 1 exists
REC1_FILT = False  # Recording for instrument 1 pos. is filtered

pygame.mixer.set_num_channels(NUM_INST * 3)  # Add more usable channels to avoid interference


# Set the instruments for the buttons in the left menu
def set_def_inst():
    for i in range(len(INSTRUMENTS)):
        if i == 0:
            INSTRUMENTS[0] = mixer.Sound(INST_DEF1)
        # if i == 0 and not REC1:
        #     print("set_def_inst() i == 0 and not REC1")
        #     INSTRUMENTS[0] = mixer.Sound(INST_DEF1)
        # elif i == 0 and REC1:  # audio1.wav must exist because recording happened
        #     print("set_def_inst() i == 0 and REC1")
        #     INSTRUMENTS[0] = mixer.Sound('audio1.wav')  # Default recording
        elif i == 1:
            INSTRUMENTS[1] = mixer.Sound(INST_DEF2)
        elif i == 2:
            INSTRUMENTS[2] = mixer.Sound(INST_DEF3)
        elif i == 3:
            INSTRUMENTS[3] = mixer.Sound(INST_DEF4)
        elif i == 4:
            INSTRUMENTS[4] = mixer.Sound(INST_DEF5)
        elif i == 5:
            INSTRUMENTS[5] = mixer.Sound(INST_DEF6)


# Set default sounds for recorded audio
def set_def_rec():
    pass


def set_filtered_inst():
    inst = ''
    for i in range(len(INSTRUMENTS)):
        if i == 0:
            inst = INST_DEF1
        elif i == 1:
            inst = INST_DEF2
        elif i == 2:
            inst = INST_DEF3
        elif i == 3:
            inst = INST_DEF4
        elif i == 4:
            inst = INST_DEF5
        elif i == 5:
            inst = INST_DEF6

        # print(f"set_filtered_inst() inst {inst}")
        audio = wave.open(inst)
        samples = audio.getnframes()
        data = audio.readframes(samples)
        audio_as_np_int16 = np.frombuffer(data, dtype=np.int16)
        filtered_audio = np.clip(audio_as_np_int16, a_min=-8192, a_max=8192)
        new_inst = inst.replace('.wav', '-filt.wav').replace('sounds/', '')
        # print(f"new_inst {new_inst}")
        wavfile.write(new_inst, samples, filtered_audio)
        INSTRUMENTS[i] = mixer.Sound(new_inst)


# Set filtered sounds for recorded audio
def set_filtered_rec():
    pass


# Set instruments to default sounds
def generate_inst():
    INSTRUMENTS.append(mixer.Sound(INST_DEF1))
    INSTRUMENTS.append(mixer.Sound(INST_DEF2))
    INSTRUMENTS.append(mixer.Sound(INST_DEF3))
    INSTRUMENTS.append(mixer.Sound(INST_DEF4))
    INSTRUMENTS.append(mixer.Sound(INST_DEF5))
    INSTRUMENTS.append(mixer.Sound(INST_DEF6))


# Create a list of beats/instruments that are all -1 (unclicked) then
# updated in main loop if clicked (changed to +1)
clicked = [[-1 for _ in range(BEATS)] for _ in range(NUM_INST)]

# Instruments selected by user in left instrument menu
# All are inactive for recording to start, and have default instrument selected
active_instruments = [1 for _ in range(NUM_INST)]


# Record audio for audio1 - audio5 to replace default instrument sound
# If filt-opt is false, use default sounds, if filt-opt true, use filtered audio
def record(audio_num):
    # if not filt_opt:
    #     print('record()')
        audio_track = 'audio' + str(audio_num + 1) + '.wav'
        mic_input = sd.rec(frames=int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1)
        sd.wait()
        wavfile.write(audio_track, SAMPLERATE, mic_input)
    # else:
    #     audio_track = 'audio' + str(audio_num + 1) + '-filt.wav'
    #     filtered = np.clip(mic_input, a_min=-8192, a_max=8192)
        # filtered_track = audio_track.replace('.wav', '-filt.wav')
        # wavfile.write(audio_track, SAMPLERATE, filtered)


# Record audio to replace instrument sound
def rec_new_sound(inst_num):
    record(inst_num)
    if inst_num == 0:
        INSTRUMENTS[i] = mixer.Sound('audio1.wav')
    if inst_num == 1:
        INSTRUMENTS[i] = mixer.Sound('audio2.wav')
    if inst_num == 2:
        INSTRUMENTS[i] = mixer.Sound('audio3.wav')
    if inst_num == 3:
        INSTRUMENTS[i] = mixer.Sound('audio4.wav')
    if inst_num == 4:
        INSTRUMENTS[i] = mixer.Sound('audio5.wav')
    if inst_num == 5:
        INSTRUMENTS[i] = mixer.Sound('audio6.wav')


# Play default tr505 and tr808 drum samples
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
    left_menu = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 5)
    bottom_menu = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200], 5)
    music_pad_grid = []
    colors = [dark_gray, roland_yellow, dark_gray]

    # Draw instrument buttons
    for i in range(NUM_INST):
        pygame.draw.rect(screen, roland_red, [0, (i*100), 200, 100], 0, 5)
        pygame.draw.line(screen, black, (0, (i * 100) + 100),  (200, (i * 100) + 100), 7)

    # Draw instrument text
    if active_inst[0] == 1:  # Default instrument
        screen.blit(label_font.render(INST_DEF1_NAME, True, colors[active_inst[0]]), (30, 30))
    elif active_inst[0] == -1:  # Use recording instead
        screen.blit(label_font.render('REC 1', True, colors[active_inst[0]]), (30, 30))
    if active_inst[1] == 1:
        screen.blit(label_font.render(INST_DEF2_NAME, True, colors[active_inst[1]]), (30, 130))
    elif active_inst[1] == -1:
        screen.blit(label_font.render('REC 2', True, colors[active_inst[1]]), (30, 130))
    if active_inst[2] == 1:
        screen.blit(label_font.render(INST_DEF3_NAME, True, colors[active_inst[2]]), (30, 230))
    elif active_inst[2] == -1:
        screen.blit(label_font.render('REC 3', True, colors[active_inst[2]]), (30, 230))
    if active_inst[3] == 1:
        screen.blit(label_font.render(INST_DEF4_NAME, True, colors[active_inst[3]]), (30, 330))
    elif active_inst[3] == -1:
        screen.blit(label_font.render('REC 4', True, colors[active_inst[3]]), (30, 330))
    if active_inst[4] == 1:
        screen.blit(label_font.render(INST_DEF5_NAME, True, colors[active_inst[4]]), (30, 430))
    elif active_inst[4] == -1:
        screen.blit(label_font.render('REC 5', True, colors[active_inst[4]]), (30, 430))
    if active_inst[5] == 1:
        screen.blit(label_font.render(INST_DEF6_NAME, True, colors[active_inst[5]]), (30, 530))
    elif active_inst[5] == -1:
        screen.blit(label_font.render('REC 6', True, colors[active_inst[5]]), (30, 530))

    # Draw music pad squares
    for i in range(BEATS):
        for j in range(NUM_INST):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = silver_blue
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // BEATS) + 205, (j * 100) + 5,
                                                    ((WIDTH - 200) // BEATS) - 10,
                                                    ((HEIGHT - 200) // NUM_INST) - 10], 0, 5)
            pygame.draw.rect(screen, silver_blue, [i * ((WIDTH - 200) // BEATS) + 200, (j * 100), ((WIDTH - 200) // BEATS),
                                            ((HEIGHT - 200) // NUM_INST)], 5, 10)
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // BEATS) + 200, (j * 100), ((WIDTH - 200) // BEATS),
                                             ((HEIGHT - 200) // NUM_INST)], 2, 5)

            music_pad_grid.append((rect, (i, j)))  # Return rectangle for each beat & coordinate for collision detection

            # Highlight current beat
            active_col = pygame.draw.rect(screen, roland_yellow, [beat * ((WIDTH - 200) // BEATS) + 200, 0,
                                                         ((WIDTH - 200) // BEATS), NUM_INST * 100], 10, 10)
    return music_pad_grid


# Main game loop modifiers
playing = True
beat_changed = True
filtering = False
active_beat = 1
active_length = 0

generate_inst()  # Set default instruments
run = True
# Main game loop
while run:
    TIMER.tick(FPS)
    screen.fill(black)  # background
    # clicked tells draw_grid which boxes to turn on/off
    music_pads = draw_grid(clicked, active_beat, active_instruments)

    ''' ~ Lower menu buttons ~ '''
    # Play/Pause button
    play_pause = pygame.draw.rect(screen, roland_red, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font2.render('Play/Pause', True, roland_yellow)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text_opt = medium_font.render('Playing', True, dark_gray)
    else:
        play_text_opt = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text_opt, (105, HEIGHT - 90))
    # BPM button
    bpm_rect = pygame.draw.rect(screen, roland_yellow, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Min', True, white)
    screen.blit(bpm_text, (325, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{BPM}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, roland_red, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, roland_red, [510, HEIGHT - 100, 48, 48], 0, 5)
    add_text = medium_font.render('+10', True, roland_yellow)
    sub_text = medium_font.render('-10', True, roland_yellow)
    screen.blit(add_text, (515, HEIGHT - 140))
    screen.blit(sub_text, (515, HEIGHT - 90))
    # Beats button
    beats_rect = pygame.draw.rect(screen, roland_yellow, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (625, HEIGHT - 130))
    beats_text2 = label_font.render(f'{BEATS}', True, white)
    screen.blit(beats_text2, (670, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, roland_red, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, roland_red, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, roland_yellow)
    sub_text2 = medium_font.render('-1', True, roland_yellow)
    screen.blit(add_text2, (815, HEIGHT - 140))
    screen.blit(sub_text2, (815, HEIGHT - 90))
    # Square Wave Filter button
    filter_rect = pygame.draw.rect(screen, roland_red, [900, HEIGHT - 150, 200, 100], 0, 5)
    filter_text = label_font2.render('Square Wave', True, roland_yellow)
    screen.blit(filter_text, (910, HEIGHT - 130))
    if filtering:
        filtering_opt = medium_font.render('On', True, dark_gray)
    else:
        filtering_opt = medium_font.render('Off', True, dark_gray)
    screen.blit(filtering_opt, (980, HEIGHT - 90))
    # Filter button
    filter2_rect = pygame.draw.rect(screen, roland_red, [1150, HEIGHT - 150, 200, 100], 0, 5)
    filter2_text = label_font2.render('Filter2', True, roland_yellow)
    screen.blit(filter2_text, (1200, HEIGHT - 130))
    if filtering:
        filtering2_opt = medium_font.render('On', True, dark_gray)
    else:
        filtering2_opt = medium_font.render('Off', True, dark_gray)
    screen.blit(filtering2_opt, (1230, HEIGHT - 90))

    # Invisible instrument rect buttons for interaction
    instrument_rects = []
    for i in range(NUM_INST):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)

    # Play instruments on each beat
    if beat_changed:
        play_notes(active_beat)
        beat_changed = False

    ''' ~ Event handling for clicking buttons ~ '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Music pad buttons pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(music_pads)):
                if music_pads[i][0].collidepoint(event.pos):
                    pad_location = music_pads[i][1]
                    # Select a box by making it positive, unselect it by making it negative
                    clicked[pad_location[1]][pad_location[0]] *= -1
        # Menu buttons pressed
        if event.type == pygame.MOUSEBUTTONUP:
            # Play/Pause button
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            # BPM add/sub button pressed (default = 240)
            elif bpm_add_rect.collidepoint(event.pos):
                BPM += 10
            elif bpm_sub_rect.collidepoint(event.pos):
                BPM -= 10
            # Beats add/sub button pressed (default = 8)
            elif beats_add_rect.collidepoint(event.pos):
                BEATS += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)  # Add column of inactive pads
            elif beats_sub_rect.collidepoint(event.pos):
                BEATS -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)  # Remove right-most column of pads
            # Filter button pressed
            elif filter_rect.collidepoint(event.pos):
                if filtering:
                    set_def_inst()
                    filtering = False
                elif not filtering:
                    set_filtered_inst()
                    filtering = True

            ''' ~ Instrument button pressed ~ '''
            for i in range(len(instrument_rects)):
                # Instrument has been recorded over
                if instrument_rects[i].collidepoint(event.pos):
                    active_instruments[i] *= -1  # turn on/off
                    # If instrument clicked, record new sound and use instead
                    if active_instruments[i] == -1:  # 1 -> def. instr. -1 -> rec. instr.
                        rec_new_sound(i)
                        # if i == 0:
                        #     if not filtering:
                        #         REC1 = True
                        #         REC1_FILT = False
                        #     if filtering:
                        #         REC1_FILT = True
                        #         REC1 = False
                        print("Instrument button pressed, change_notes()")
                    # Instrument is not a recording
                    else:
                        if i == 0:
                            # REC1 = False
                            INSTRUMENTS[i] = mixer.Sound(INST_DEF1)
                        if i == 1:
                            INSTRUMENTS[i] = mixer.Sound(INST_DEF2)
                        if i == 2:
                            INSTRUMENTS[i] = mixer.Sound(INST_DEF3)
                        if i == 3:
                            INSTRUMENTS[i] = mixer.Sound(INST_DEF4)
                        if i == 4:
                            INSTRUMENTS[i] = mixer.Sound(INST_DEF5)
                        if i == 5:
                            INSTRUMENTS[i] = mixer.Sound(INST_DEF6)

    # Cycle through music pad columns for num of beats
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
