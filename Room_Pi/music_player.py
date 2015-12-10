# play a music file using module pygame
# (does not create a GUI frame for now)
# Muzi

#play a list in order

import sys
import pygame as pg
import getopt


class music_player(object):
    def __init__(self):#build a playlist and play it in order
        print "1111111"
        #sys.path.append('/path/to/~/Documents/Music_player/playlist/') #from another folder
        self.play_list_END = self.pg.USEREVENT+1
        file = open('playlist.txt','r') #Three sound effects I have
        #lines = file.readlines()
        self.play_list = []
        for line in file :
            self.play_list.append(line.split("\n")[0])
            print "line in file",line
        #file.close()
        print "playlist",self.play_list
        self.index = 0
        self.song_volume = 0.2 #default volume
        self.pg.init()#init pygame
        #pg.display.set_mode((500,500)) #menu window
        self.pg.mixer.music.set_volume(self.song_volume)# set default volume
        self.pg.mixer.music.set_endevent(self.play_list_END)#used to check song ends
        pg.mixer.music.load(self.play_list[0])#start from the very first song

        self.music_status = "stop" #stop  playing
        self.track_name = '' #track song name, the default is the first one in playlist


    #Let user change volume
    def change_volume(self,voice_command):
        self.pg.mixer.music.set_volume(self.song_volume)
        if voice_command == "increase":
            self.song_volume += 0.1
        elif voice_command == "decrease":
            self.song_volume -= 0.1
        else:
            self.song_volume = 0.2  #default if no "change" command received

    #when it's going to stop (not like pause)
    def music_fadeout(self):
        pg.mixer.fadeout(5)
        self.play_list[self.index].play()


    #activate the player and start playing music
    def activate_player(self)#,voice_command):
        # if voice_command == 'play':
        #     print"Player activated"
            #call init_player
            self.pg.mixer.music.play()
            self.music_status = "playing"
            self.track_name = self.play_list[self.index]
            #check the end of a event(here i.e. song) if true then go to next track.
            while 1:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.pg.quit()
                        sys.exit()
                    elif event.type == self.play_list_END:
                        self.index = (self.index+1)%len(self.play_list) #recycle the playlist when the last song is playing
                        self.pg.mixer.music.load(self.play_list[self.index])
                        self.pg.mixer.music.play()
        #print "Playing music"
        #what if not activated ????

    #play the next song in list
    def go_next(self,voice_command):
        if self.pg.mixer.get_busy() : #currently playing
            self.pg.mixer.music.pause()
        print"Playing next song~~"
        self.index += 1 #point to the next
        if self.index >= len(self.play_list): #in case it's the last song in list
            self.index = 0
            #if not self.loop:
            #playNextSong = False
            self.pg.mixer.music.stop()
            #self.loadSong()
        self.track_name = self.play_list[self.index] #track the next song name
        self.pg.mixer.music.load(self.play_list[self.index])
        self.pg.mixer.music.play()

    #pause it
    def pause(self):
        """
        Pauses the current song.

        You can resume using `un_pause/play`.
        """
        self.pg.mixer.music.pause()
        self.music_status = 'Pause'
        #self.playing = False

    def un_pause(self):
        self.pg.mixer.music.unpause()
        self.music_status = "playing"
        #self.playing = True # Does it work? or need to reload music?
        #pg.mixer.music.load(self.play_list[self.index])#start from the very first song
        #pg.mixer.music.play()

    def stop(self):
        #Stops the current song and goes to the beginning.
        self.pg.mixer.music.stop()
        self.music_status = "stopped"
        self.index = 0 #back to beginning of list(default 0)

    def previousSong(self):
        #Returns to the previous song in the playlist.
        if self.pg.mixer.get_busy() : #currently playing
            self.pg.mixer.music.pause()
        print"Playing previous song~~"
        self.index -= 1
        if self.index < 0:
            self.index = len(self.play_list) - 1
            self.stop()
        self.track_name = self.play_list[self.index]
        self.pg.mixer.music.load(self.track_name)
        self.pg.mixer.music.play()

#
# def main(self):     # parse command line options
#     try:
#         opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
#     except getopt.error, msg:
#         print msg
#         print "for help use --help"
#         sys.exit(2)
#     # process options
#     for o, a in opts:
#         if o in ("-h", "--help"):
#             print __doc__
#             sys.exit(0)
#     # process arguments
#     for arg in args:
#         go_next(arg)
#
#
# if __name__=="__main__":
#     main()
#     music_test = music_player() #Test to call this player class
#     voice_command = (sys.argv[1:])
