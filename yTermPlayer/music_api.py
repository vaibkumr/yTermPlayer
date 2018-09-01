import pafy
import vlc
import pickle
import sys
import os
import time
import threading
from random import randint
from .settings import PL_DIR


class YoutubePlayer:
    def __init__(self):
        #URL of list
        self.url=""
        #Set unlock on continous_player
        self._lock=False
        #Open the paylists dict from pickle here
        self.saved_lists=[]
        #Currently playing song name
        self._currentSong="None"
        ### FIX THIS!!! INDEX STARTING FROM ZERO MUST BE ALLOWED TO BE PLAYED!!!!
        self.index=0
        ## new playlist?
        self._new=True
        #Define queue length
        self.queue_len=0
        #Define repeat mode 1=Repeat off | 2=Repeat current song | 3=Repeat list.
        #By default repeat is off
        self.repeat_mode=1
        #Define random 0=Random off | 1=Random on
        self.random=0
        #This lock is for locking in case music is paused intentionlly
        self._togglerLock=False
        #Make time details dict
        self.time_details={}
        #Random on or off?
        self._random=False
        #This is changed to true by the continous player and then back to false by an event handler
        self._song_changed=False
        self.path=os.path.split(os.path.abspath(__file__))[0]
        for every_file in os.listdir(PL_DIR):
            # print("Directories checked")
            self.saved_lists.append(every_file)
        #Initialize VLC player
        self.player = vlc.MediaPlayer()
        # print("Player Initialized")
        #Put playlists as empty

    def get_index(self):
        return self.index

    def set_repeat_mode(self,mode):
        #If invalid, set return mode to no repeat
        if(int(mode) not in [1,2,3]):
            self.repeat_mode=1
        else:
            self.repeat_mode=int(mode)

    def play_random(self):
        if(self._random):
            self._random=False
        else:
            self._random=True

    def get_repeat_mode(self):
        return self.repeat_mode

    def initPlaylist(self,url):
        self.url=url
        self.playlist=pafy.get_playlist(url)
        self.queue_len=len(self.playlist['items'])

    def save_current_list(self):
        try:
            filename=PL_DIR+"/"+self.playlist['title']
        except:
            return False
        self.saved_lists.append(filename)
        with open(filename,'wb') as handler:
            pickle.dump({'url':self.url,'name':self.playlist['title']}, handler, pickle.HIGHEST_PROTOCOL)
        return True

    def load_saved_playlist(self,list_name):
        if list_name not in self.saved_lists:
            return False
        #Load list pickle object
        filename=PL_DIR+"/"+list_name
        with open(filename,'rb') as handler:
            url=pickle.load(handler)['url']
        self.playlist=pafy.get_playlist(url)
        self.queue_len=len(self.playlist['items'])
        return True

    def get_saved_lists(self):
        return self.saved_lists

    def get_list_data(self):
        self.list_data=[]
        ##In case of empty/inexistent list
        if(not self.playlist):
            return self.list_data
        for every_object in self.playlist['items']:
            self.temp={}
            self.temp["title"]=str(every_object['pafy'].title)
            self.temp['author']=str(every_object['pafy'].author)
            time=str(every_object['pafy'].duration).split(":")
            hours=int(time[0])
            minutes=int(time[1])
            seconds=int(time[2])
            if(seconds<10 and hours==0 and minutes<10):
                self.temp['duration']="0"+str(minutes)+":0"+str(seconds)
            elif(hours==0 and minutes<10):
                self.temp['duration']="0"+str(minutes)+":"+str(seconds)
            elif(seconds<10):
                self.temp['duration']=str((hours*60)+minutes)+":0"+str(seconds)
            else:
                self.temp['duration']=str((hours*60)+minutes)+":"+str(seconds)
            self.list_data.append(self.temp)
        return self.list_data

    def get_url_and_name(self,index):
        try:
            return [self.playlist['items'][int(index)]['pafy'].getbestaudio().url,self.playlist['items'][int(index)]['pafy'].title]
        except IndexError:
            return False

    def get_next_index(self):
        if(self._random):
            self.next_index=randint(1,int(self.queue_len)-1)
            return int(self.next_index)

        self.index=int(self.index)
        self.queue_len=int(self.queue_len)
        #repeat playlist
        if(self.repeat_mode==3):
            if(self.index==self.queue_len-1 or self.index>self.queue_len ):
                self.next_index=0
            else:
                self.next_index=self.index+1
        #repeat single song
        elif(self.repeat_mode==2):
            self.next_index=self.index
        #no repeat mode
        else:
            if(self.index==self.queue_len-1):
                self.next_index=False
            else:
                self.next_index=self.index+1
        return int(self.next_index)

    def get_prev_index(self):
        self.index=int(self.index)
        if(self.index<=0):
            self.prev_index=-1
        else:
            self.prev_index=self.index-1
        return int(self.prev_index)

    def play_at_index(self,index):
        self._song_changed=True
        self._new=False
        self._lock=True
        self.index=index
        #Play current index
        details=self.get_url_and_name(index)
        url=details[0]
        self._currentSong=details[1]

        if(url==False):
            return False
        # print("i am playing: ",index)
        self.player.set_mrl(url)
        self.player.play()
        #Remove lock on continous_player
        while(not self.player.is_playing()):
            self._lock=True
        self._lock=False
        return True

    def stop(self):
        self._lock=True
        self.player.stop()

    def get_playlist_name(self):
        return self.playlist['title']

    def get_time_details(self):
        time_seconds1=int(int(self.player.get_length())/1000)
        self.time_details['total_time']=str(int(time_seconds1/60))+":"+str(time_seconds1%60)
        minutes=int(time_seconds1/60)
        seconds=time_seconds1%60
        if(seconds<10 and minutes<10):
            self.time_details['total_time']="0"+str(minutes)+":0"+str(seconds)
        elif(minutes<10):
            self.time_details['total_time']="0"+str(minutes)+":"+str(seconds)
        elif(seconds<10):
            self.time_details['total_time']=str(minutes)+":0"+str(seconds)
        else:
            self.time_details['total_time']=str(minutes)+":"+str(seconds)

        time_seconds2=int(int(self.player.get_time())/1000)
        minutes=int(time_seconds2/60)
        seconds=time_seconds2%60
        if(seconds<10 and minutes<10):
            self.time_details['cur_time']="0"+str(minutes)+":0"+str(seconds)
        elif(minutes<10):
            self.time_details['cur_time']="0"+str(minutes)+":"+str(seconds)
        elif(seconds<10):
            self.time_details['cur_time']=str(minutes)+":0"+str(seconds)
        else:
            self.time_details['cur_time']=str(minutes)+":"+str(seconds)

        if(time_seconds1 is not 0):
            self.time_details['percentage']=(time_seconds2/time_seconds1)*100
        else:
            self.time_details['percentage']=0

        return self.time_details

    def start_playing(self):
        thread=threading.Thread(target=self.continous_player, args={})
        thread.daemon = True
        thread.start()

    def continous_player(self):
        while(True):
            time.sleep(2)
            if(self._togglerLock):
                continue
            if(self.player.is_playing()==False and self._lock==False):
                self._lock=True
                if(self._new):
                    self._new=False
                    self.index=0
                    self.play_at_index(0)
                else:
                    _next = self.get_next_index()
                    if(_next):
                        self.play_at_index(int(_next))
                    else:
                        # print("i've stoppped it!")
                        self.stop()
                self._song_changed=True

    def play_next(self):
        self.stop()
        _next_index=self.get_next_index()
        if(not _next_index):
            return False
        self.play_at_index(_next_index)

    def play_prev(self):
        self.stop()
        _prev_index=self.get_prev_index()
        if(_prev_index==-1):
            # print("nothing previous here")
            return False
        self.play_at_index(_prev_index)

    def current_song_name(self):
        return self._currentSong

    def toggle_playing(self):
        if(self.player.is_playing()):
            self._togglerLock=True
            self.player.pause()
        else:
            self.player.play()
            time.sleep(1)
            self._togglerLock=False

#GRAVEYARD
#TESTING
# if __name__=="__main__":
#     player_object=YoutubePlayer()
#     print("Object made")
#     #player_object.initPlaylist("https://www.youtube.com/playlist?list=PLHLDQyQ-L9cSk--81-S01IdYXRilDbpeH")
#     player_object.initPlaylist("https://www.youtube.com/playlist?list=PLHLDQyQ-L9cRjRjBJCBJOJ9MeMHpLY-oe")
#     print("Playlist Initialized")
#     player_object.set_repeat_mode(2)
#
#     # player_object.load_saved_playlist("animu")
#     ch=""
#     input("Show data [ENTER] ")
#     xyz=player_object.get_list_data()
#     for a in xyz:
#         print(a)
#     player_object.save_current_list()
#     print("started playing ")
#     player_object.start_playing()
#
#     while(ch!="-1"):
#         print("this it??",player_object.current_song_name())
#         ch=input("n? p? ")
#         if(ch=="n"):
#             print("Next!")
#             player_object.play_next()
#         elif(ch=="p"):
#             player_object.play_prev()
#         elif(int(ch)==-1):
#             exit()
#         else:
#             player_object.play_at_index(int(ch))
