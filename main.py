# Yuriy Alexander
# CS410 Computers, Sound & Music
# Final Project

import simpleaudio as sa


def print_wav(file):
    wave_obj = sa.WaveObject.from_wave_file(file)
    play_obj = wave_obj.play()
    play_obj.wait_done()


if __name__ == '__main__':
    print_wav('clap.wav')
    print_wav('crash.wav')
    print_wav('hi hat.wav')
    print_wav('snare.wav')
    print_wav('tom.wav')
    print_wav('kick.wav')

