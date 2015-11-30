# play a MP3 music file using module pygame
# (does not create a GUI frame for now)
# Muzi

import pygame

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print "Music file %s loaded!" % music_file
    except pygame.error:
        print "File %s not found! (%s)" % (music_file, pygame.get_error())
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


# pick a MP3 file ...
# (if not in working folder, use full path--which is a pain)
music_file = "Hello.mp3"
#music_file = "Adele-Hello.mp3"

# set up the mixer(needed since mp3 support is limited or sth Idk)
freq = 44100     # audio CD quality
bitsize = -16    # unsigned 16 bit
channels = 2     # 1 is mono, 2 is stereo works for earphone
buffer = 2048    # number of samples (experiment to get right sound)
pygame.mixer.init(freq, bitsize, channels, buffer)

# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.75)

try:
    play_music(music_file)
except KeyboardInterrupt:
    # if user hits Ctrl/C then exit
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit
