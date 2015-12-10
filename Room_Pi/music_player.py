# play a music file using module pygame
# (does not create a GUI frame for now)
# Muzi

#play a list in order


        import sys, time, threading
import pygame as pg
import getopt


class music_player():
    def __init__(self):#build a playlist and play it in order
        print "1111111"
        #sys.path.append('/path/to/~/Documents/Music_player/playlist/') #from another folder
        self.play_list_END = pg.USEREVENT+1
        self.MusicPlayerStoped = False
        file = open('playlist.txt','r') #Three sound effects I have
        #lines = file.readlines()
        self.play_list = []
        for line in file :
            self.play_list.append(line.split("\n")[0])
            print "line in file",line
        #file.close()
        print "playlist",self.play_list
        self.index = 0
        self.MusicPlayerInterrupt = False
        self.song_volume = 0.2 #default volume
        pg.init()#init pygame
        #pg.display.set_mode((500,500)) #menu window
        pg.mixer.music.set_volume(self.song_volume)# set default volume
        pg.mixer.music.set_endevent(self.play_list_END)#used to check song ends
        pg.mixer.music.load(self.play_list[0])#start from the very first song
        pg.mixer.music.play()

        self.music_status = "stop" #stop pause playing
        self.track_name = {} #track song name, the default is the first one in playlist
        #check the end of a event(here i.e. song) if true then go to next track.
        mpthread = threading.Thread(target=self.checkMusicPlayer)
        mpthread.daemon = True
        mpthread.start()



        # while 1:
        #     for event in pg.event.get():
        #         if event.type == pg.QUIT:
        #             pg.quit()
        #             sys.exit()
        #         elif event.type == self.play_list_END:
        #             self.index = (self.index+1)%len(self.play_list) #recycle the playlist when the last song is playing
        #             pg.mixer.music.load(self.play_list[self.index])
        #             pg.mixer.music.play()

    def checkMusicPlayer(self):
        while self.index in range(0, len(self.play_list)):
            while pg.mixer.music.get_busy():
                continue

            while self.MusicPlayerStoped == True:
                continue

            if (self.index) < len(self.play_list)-1:
                self.index = self.index + 1
            else:
                self.index = 0
            pg.mixer.music.load(self.play_list[self.index])
            self.track_name = self.play_list[self.index]
            print 'Current song information', self.track_name
            pg.mixer.music.play()

    #Increase music player volume
    def raise_volume(self):
        self.song_volume = self.song_volume + 0.2
        pg.mixer.music.set_volume(self.song_volume)

    #Decrease music player volume
    def decrease_volude(self):
        self.song_volume = self.song_volume - 0.2
        pg.mixer.music.set_volume(self.song_volume)

    #when it's going to stop (not like pause)
    def music_fadeout(self):
        self.pg.mixer.fadeout(5)
        self.play_list[self.index].play()


    #activate the player and start playing music
    def activate_player(self):
        print"Player activated"
        pg.mixer.music.play()
        #call init_player
        self.MusicPlayerStoped = False
        self.music_status = "playing"
        self.track_name = self.play_list[self.index]
        print "Play awaiting"
        #what if not activated ????

    #play the next song in list
    def go_next(self):
        if pg.mixer.get_busy() : #currently playing
            pg.mixer.music.pause()
        print"Playing next song~~"
        # self.index+=1 #point to the next
        if self.index >= len(self.play_list): #in case it's the last song in list
            self.index = 0
            pg.mixer.music.stop()

        self.track_name = self.play_list[self.index] #track the next song name
        pg.mixer.music.load(self.play_list[self.index])
        pg.mixer.music.play()

    #pause it
    def pause(self):
        """
        Pauses the current song.

        You can resume using `un_pause/play`.
        """
        pg.mixer.music.pause()
        self.music_status = "paused"
        #self.playing = False

    def un_pause(self):
        pg.mixer.music.unpause()
        self.music_status = "playing"
        #self.playing = True # Does it work? or need to reload music?
        #pg.mixer.music.load(self.play_list[self.index])#start from the very first song
        #pg.mixer.music.play()

    def stop(self):
        #Stops the current song and goes to the beginning.
        pg.mixer.music.stop()
        self.MusicPlayerStoped = True
        self.music_status = "stopped"
        self.index = 0 #back to beginning of list(default 0)

    def previousSong(self):
        #Returns to the previous song in the playlist.
        if pg.mixer.get_busy() : #currently playing
            pg.mixer.music.pause()
        # self.stop()
        print"Playing previous song~~"
        self.index -= 2
        if self.index < 0:
            self.index = len(self.play_list) - 1
            #self.stop()
        self.track_name = self.play_list[self.index]
        pg.mixer.music.load(self.track_name)
        pg.mixer.music.play()


#
if __name__=="__main__":
    # main()
    music_test = music_player() #Test to call this player class
    while 1:
        time.sleep(10)
        print 'Pause!!!!!'
        music_test.pause()
        time.sleep(3)
        print 'next song'
        music_test.go_next()
        time.sleep(8)
        print 'pause!!!!'
        music_test.pause()
        time.sleep(8)
        print 'pervious song!!!!'
        music_test.previousSong()
        time.sleep(5)
        print 'un_pause!!!!'
        music_test.un_pause()
        time.sleep(4)
        print 'next song!!!!'
        music_test.go_next()
        time.sleep(2)
        print 'volume up!!!!'
        music_test.raise_volume()
        time.sleep(10)
        print 'volume down!!!'
        music_test.decrease_volude()
        time.sleep(10)

#
#
#         #music_test.MusicPlayerInterrupt = True
#     #music_player.MusicPlayerInterrupt = True
#     #voice_command = (sys.argv[1:])
