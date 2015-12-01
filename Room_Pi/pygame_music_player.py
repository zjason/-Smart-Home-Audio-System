import pygame
import time

pygame.mixer.init()
pygame.display.init()

#screen = pygame.display.set_mode ( ( 420 , 240 ) )

playlist = list()#reversed order ??? wtf
playlist.append ( "GLADES_-_Her_Loving_You_.ogg" )#music #3
playlist.append ( "Adele - Hello.ogg" )#music #2
playlist.append ( "Chris Brown - Don't Judge Me.ogg" )#music #1


song = playlist.pop()
print "Loading song: {}".format(song)
pygame.mixer.music.load ( song )  # Get the first track from the playlist
song = playlist.pop()
print "Queuing song: {}".format(song)
pygame.mixer.music.queue ( song ) # Queue the 2nd song
pygame.mixer.music.set_endevent ( pygame.USEREVENT )    # Setup the end track event
print "Playing first track"
pygame.mixer.music.play()           # Play the music

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:    # A track has ended
            print "Track has ended"
            if playlist:       # If there are more tracks in the queue... (A non-empty list is True)
                print "Songs left in playlist@ {}".format(len(playlist))
                song = playlist.pop()
                print "Queuing next song: {}".format(song)
                pygame.mixer.music.queue ( song ) # Queue the next one in the list
            else:
                print "Playlist is empty"
