# play a music file using module pygame
# (does not create a GUI frame for now)
# Muzi

import sys
import pygame as pg

#play a list in order

import sys
import pygame as pg

class music_player():
    def __init__(self):#build a playlist and play it in order
        print "1111111"
        #sys.path.append('/path/to/~/Documents/Music_player/playlist/') #from another folder
        self.play_list_END = pg.USEREVENT+1
        file = open('playlist.txt','r') #Three sound effects I have
        #lines = file.readlines()
        self.play_list = []
        for line in file :
            self.play_list.append(line.split("\n")[0])
            print "line in file",line
        #file.close()
        print "playlist",self.play_list
        song = 0
        self.index = 0
        song_volume = 0.2 #default volume
        pg.init()#init pygame
        #pg.display.set_mode((500,500)) #menu window
        pg.mixer.music.set_volume(song_volume)# set default volume
        pg.mixer.music.set_endevent(self.play_list_END)#used to check song ends
        pg.mixer.music.load(self.play_list[0])#start from the very first song
        pg.mixer.music.play()

        self.music_status = "stop" #stop pause playing
        self.track_name = self.play_list[count] #track song name, the default is the first one in playlist
        #check the end of a event(here i.e. song) if true then go to next track.
        while 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == self.play_list_END:
                    song = (song+1)%len(self.play_list) #recycle the playlist when the last song is playing
                    pg.mixer.music.load(self.play_list[song])
                    pg.mixer.music.play()


    #Let user change volume
    def change_volume(self,vol):
        song_volume = vol
        pg.mixer.music.set_volume(song_volume)

    #activate the player and start playing music
    def activate_player(self,activate_command):
        if activate_command == 'activate':
            print"Player activated"
            #call init_player
            self.music_status = "playing"
        print "Play awaiting"

    #play the next song in list
    def go_next(self):
        print"Playing next song~~"
        self.index+=1
        self.track_name = self.play_list[self.index+1] #track the next song name

    #pause it
    def pause(self):
        """
        Pauses the current song.

        You can resume using `play`.
        """
        pg.mixer.music.pause()
        self.playing = False

    def un_pause(self):
        pg.mixer.music.unpause()
        self.music_status = "playing"
        #self.playing = True # Does it work? or need to reload music?
        #pg.mixer.music.load(self.play_list[self.index])#start from the very first song
        #pg.mixer.music.play()

    def stop(self):
        #Stops the current song and goes to the beginning.
        pg.mixer.music.stop()
        self.playing = False

    def previousSong(self):
        #Returns to the previous song in the playlist.
        if self.play_list:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.play_list) - 1
            self.stop()
        self.track_name = self.play_list[self.index]

            #self.loadSong()

    def nextSong(self):
        if self.play_list:
            playNextSong = self.playing
            self.index += 1
            if self.index >= len(self.play_list):
                self.index = 0
                #if not self.loop:
                    #playNextSong = False
            self.stop()
            #self.loadSong()
            if playNextSong:
                self.play()




music_test = music_player() #TEst to call this player class
