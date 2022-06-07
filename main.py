# Yuriy Alexander
# CS410 Computers, Sound & Music
# Final Project
# Project demo: https://www.youtube.com/watch?v=duexxwhxclM

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
DURATION = 0.6
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

pygame.mixer.set_num_channels(NUM_INST * 3)  # Add more usable channels to avoid interference


# Set the instruments for the buttons in the left menu
def set_def_inst():
    for i in range(len(INSTRUMENTS)):
        if i == 0:
            INSTRUMENTS[0] = mixer.Sound(INST_DEF1)
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


def set_def_rec(rec_num):
    print("set_def_rec()")
    if rec_num == 0:
        INSTRUMENTS[0] = mixer.Sound('audio1.wav')
    elif rec_num == 1:
        INSTRUMENTS[1] = mixer.Sound('audio2.wav')
    elif rec_num == 2:
        INSTRUMENTS[2] = mixer.Sound('audio3.wav')
    elif rec_num == 3:
        INSTRUMENTS[3] = mixer.Sound('audio4.wav')
    elif rec_num == 4:
        INSTRUMENTS[4] = mixer.Sound('audio5.wav')
    elif re == 5:
        INSTRUMENTS[5] = mixer.Sound('audio6.wav')


def set_reverb_inst():
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

        fs, audio = wavfile.read(inst)

        echo_dur = 0.4
        delay_amp = 0.15
        delay_samples = round(echo_dur * fs)
        zero_padding = np.zeros(delay_samples)

        delay_padding = np.concatenate((zero_padding, audio))
        delayed_audio = np.concatenate((audio, zero_padding))
        reverb_audio = delayed_audio + delay_amp * delay_padding

        new_inst = inst.replace('.wav', '-rev.wav').replace('sounds/', '')
        wavfile.write(new_inst, fs, reverb_audio.astype(np.int16))
        INSTRUMENTS[i] = mixer.Sound(new_inst)


def set_sqrwave_inst():
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

        fs, audio = wavfile.read(inst)
        filtered_audio = audio.astype(np.int16)
        filtered_audio = np.clip(filtered_audio, a_min=-2000, a_max=2000)
        new_inst = inst.replace('.wav', '-filt.wav').replace('sounds/', '')
        wavfile.write(new_inst, fs, filtered_audio)
        INSTRUMENTS[i] = mixer.Sound(new_inst)


# TO-DO
# Set filtered sounds for recorded audio
def set_sqrwave_rec(i):
    inst = ''
    if i == 1:
        inst = 'audio1.wav'
    elif i == 2:
        inst = 'audio2.wav'
    elif i == 3:
        inst = 'audio3.wav'
    elif i == 4:
        inst = 'audio4.wav'
    elif i == 5:
        inst = 'audio5.wav'
    elif i == 6:
        inst = 'audio6.wav'

    fs, audio = wavfile.read(inst)
    filtered_audio = audio.astype(np.int16)
    filtered_audio = np.clip(filtered_audio, a_min=-8192, a_max=8192)
    new_inst = inst.replace('.wav', '-filt.wav')
    wavfile.write(new_inst, fs, filtered_audio)
    INSTRUMENTS[i] = mixer.Sound(new_inst)


# TO-DO
def set_reverb_rec(rec_num):
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
        audio_track = 'audio' + str(audio_num + 1) + '.wav'
        mic_input = sd.rec(frames=int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1)
        sd.wait()
        wavfile.write(audio_track, SAMPLERATE, mic_input)


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
            mus_pad = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // BEATS) + 205, (j * 100) + 5,
                                                    ((WIDTH - 200) // BEATS) - 10,
                                                    ((HEIGHT - 200) // NUM_INST) - 10], 0, 5)
            pygame.draw.rect(screen, silver_blue, [i * ((WIDTH - 200) // BEATS) + 200, (j * 100), ((WIDTH - 200) // BEATS),
                                            ((HEIGHT - 200) // NUM_INST)], 5, 10)
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // BEATS) + 200, (j * 100), ((WIDTH - 200) // BEATS),
                                             ((HEIGHT - 200) // NUM_INST)], 2, 5)

            music_pad_grid.append((mus_pad, (i, j)))  # Return rectangle for each beat & coordinate for collision detection

            # Highlight current beat
            active_col = pygame.draw.rect(screen, roland_yellow, [beat * ((WIDTH - 200) // BEATS) + 200, 0,
                                                         ((WIDTH - 200) // BEATS), NUM_INST * 100], 10, 10)
    return music_pad_grid


# Main game loop modifiers
playing = True
beat_changed = True
sqr_filter = False
rev_filter = False
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
    # Draw Play/Pause button
    play_pause = pygame.draw.rect(screen, roland_red, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font2.render('Play/Pause', True, roland_yellow)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text_opt = medium_font.render('Playing', True, dark_gray)
    else:
        play_text_opt = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text_opt, (105, HEIGHT - 90))
    # Draw BPM button
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
    # Draw Beats button
    beats_rect = pygame.draw.rect(screen, roland_yellow, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (625, HEIGHT - 130))
    beats_text2 = label_font.render(f'{BEATS}', True, white)
    screen.blit(beats_text2, (690, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, roland_red, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, roland_red, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, roland_yellow)
    sub_text2 = medium_font.render('-1', True, roland_yellow)
    screen.blit(add_text2, (815, HEIGHT - 140))
    screen.blit(sub_text2, (815, HEIGHT - 90))
    # Draw Square Wave Filter button
    sq_wave_btn = pygame.draw.rect(screen, roland_red, [900, HEIGHT - 150, 200, 100], 0, 5)
    sq_wave_text = label_font2.render('Square Wave', True, roland_yellow)
    screen.blit(sq_wave_text, (910, HEIGHT - 130))
    if sqr_filter:
        filtering_opt = medium_font.render('On', True, dark_gray)
    else:
        filtering_opt = medium_font.render('Off', True, dark_gray)
    screen.blit(filtering_opt, (980, HEIGHT - 90))
    # Draw Filter2 button
    reverb_btn = pygame.draw.rect(screen, roland_red, [1150, HEIGHT - 150, 200, 100], 0, 5)
    reverb_text = label_font2.render('Reverb', True, roland_yellow)
    screen.blit(reverb_text, (1200, HEIGHT - 130))
    if rev_filter:
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
        # Click Music pad buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(music_pads)):
                if music_pads[i][0].collidepoint(event.pos):
                    pad_location = music_pads[i][1]
                    # Select a box by making it positive, unselect it by making it negative
                    clicked[pad_location[1]][pad_location[0]] *= -1
        # Click Menu button
        if event.type == pygame.MOUSEBUTTONUP:
            # Click Play/Pause button
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            # Click BPM add/sub button (default = 240)
            elif bpm_add_rect.collidepoint(event.pos):
                BPM += 10
            elif bpm_sub_rect.collidepoint(event.pos):
                BPM -= 10
            # Click Beats add/sub button (default = 8)
            elif beats_add_rect.collidepoint(event.pos):
                BEATS += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)  # Add column of inactive pads
            elif beats_sub_rect.collidepoint(event.pos):
                BEATS -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)  # Remove right-most column of pads
            # Click Square Wave button
            elif sq_wave_btn.collidepoint(event.pos):
                # print(f"sq_wave_btn clicked i -> {i}")
                if sqr_filter:  # Square wave button Off
                    # Set all default instruments to non-filtered sound
                    set_def_inst()
                    # Set recorded audio to non-filtered if enabled
                    # if REC1 is True:
                    #     set_def_rec(1)
                    #     REC1 = False
                    sqr_filter = False
                elif not sqr_filter:  # Square wave button On
                    # Filter all default instruments with square wave filter
                    set_sqrwave_inst()
                    # Filter recorded audio if enabled
                    # if REC1:
                    #     set_sqrwave_rec(1)
                    #     REC1 = False
                    sqr_filter = True
            # Click Reverb button
            elif reverb_btn.collidepoint(event.pos):
                if rev_filter:  # Reverb button Off
                    # Filter recorded audio if enabled
                    # if REC1:
                    #     set_reverb_rec(i)
                    # Set all default instruments to non-reverb sound
                    set_def_inst()
                    rev_filter = False
                elif not rev_filter:  # Reverb button On
                    # Set all default instruments to reverb sound
                    set_reverb_inst()
                    rev_filter = True

            ''' ~ Instrument button pressed ~ '''
            for i in range(len(instrument_rects)):
                # Instrument has been recorded over
                if instrument_rects[i].collidepoint(event.pos):
                    # if i == 0:  # hit 1st instrument box
                    #     REC1 = True
                    active_instruments[i] *= -1  # turn on/off
                    # If instrument clicked, record new sound and use instead
                    if active_instruments[i] == -1:  # 1 -> def. instr. -1 -> rec. instr.
                        if i == 0:  # if instrument is inst 1
                            REC1 = True

                        rec_new_sound(i)
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
