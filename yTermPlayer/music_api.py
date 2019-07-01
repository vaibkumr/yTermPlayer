#!/usr/bin/env python3
'''
yTermPlayer music api by TimeTraveller
(https://github.com/TimeTraveller-San/yTermPlayer)
Special thanks for these libraries and their contributors:
- urwid
- pafy
- mpv
'''
import pafy
import mpv
import pickle
import sys
import os
import time
import threading
from random import randint
import math
from .settings import PL_DIR
import locale

def structure_time(seconds, minutes, hours):
    if(seconds < 10 and hours == 0 and minutes < 10):
        structured_time = "0" + str(minutes) + ":0" + str(seconds)
    elif(hours == 0 and minutes < 10):
        structured_time = "0" + str(minutes)+ ":" + str(seconds)
    elif(seconds < 10):
        structured_time = str((hours*60) + minutes) + ":0" + str(seconds)
    else:
        structured_time = str((hours*60) + minutes) + ":" + str(seconds)
    return structured_time

def structure_time_len(seconds, minutes):
    if(seconds < 10 and minutes < 10):
        structured_time = "0" + str(minutes) + ":0" + str(seconds)
    elif(minutes < 10):
        structured_time = "0" + str(minutes) + ":" + str(seconds)
    elif(seconds < 10):
        structured_time = str(minutes) + ":0" + str(seconds)
    else:
        structured_time = str(minutes) + ":" + str(seconds)
    return structured_time

class YoutubePlayer:
    def __init__(self):
        #URL of list
        self.url = ""
        #Player volume
        self.volume = 100
        #Set unlock on continous_player
        self._lock = False
        #Semaphore for the shared _lock variable
        self._lock_mutex = threading.Semaphore()
        #Open the paylists dict from pickle here
        self.saved_lists = []
        #Currently playing song name
        self._currentSong = "None"
        ##Current song index
        self.index = 0
        ##New playlist?
        self._new = True
        #Define queue length
        self.queue_len = 0
        #Define repeat mode 1:Repeat off | 2:Repeat current song | 3:Repeat list.
        #Default mode is 1
        self.repeat_mode = 1
        #Define random 0:Random off | 1:Random on
        self.random = 0
        #This lock is for locking in case music is paused intentionlly
        self._togglerLock = False
        #Semaphore for the shared _togglerLock variable
        self._togglerLock_mutex = threading.Semaphore()
        #Make time details dict
        self.time_details = {}
        #Random on or off?
        self._random = False
        # This is changed to true by the continous player and then back to
        # false by an event handler
        self._song_changed = False
        self.path = os.path.split(os.path.abspath(__file__))[0]
        for every_file in os.listdir(PL_DIR):
            self.saved_lists.append(every_file)
        #Initialize MPV player
        locale.setlocale(locale.LC_NUMERIC, "C")
        self.player = None


    def get_index(self):
        return self.index

    def set_repeat_mode(self, mode):
        #If invalid, set return mode to no repeat
        if(int(mode) not in [1,2,3]):
            self.repeat_mode = 1
        else:
            self.repeat_mode = int(mode)

    def play_random(self):
        if(self._random):
            self._random = False
        else:
            self._random = True

    def get_repeat_mode(self):
        return self.repeat_mode

    def initPlaylist(self,url):
        self.url = url
        self.playlist = pafy.get_playlist(url)
        self.queue_len = len(self.playlist['items'])

    def save_current_list(self):
        try:
            filename = PL_DIR + "/" + self.playlist['title']
        except:
            return False
        self.saved_lists.append(filename)
        with open(filename,'wb') as handler:
            pickle.dump({
                        'url' : self.url,
                        'name' : self.playlist['title']
                        },
                        handler,pickle.HIGHEST_PROTOCOL)
        return True

    def load_saved_playlist(self, list_name):
        if list_name not in self.saved_lists:
            return False
        #Load list pickle object
        filename = PL_DIR +"/" + list_name
        with open(filename,'rb') as handler:
            url = pickle.load(handler)['url']
        self.playlist = pafy.get_playlist(url)
        self.queue_len = len(self.playlist['items'])
        return True

    def get_saved_lists(self):
        return self.saved_lists

    def get_list_data(self):
        self.list_data = []
        ##In case of empty/inexistent list
        if(not self.playlist):
            return self.list_data
        for every_object in self.playlist['items']:
            temp_details = {}
            temp_details["title"] = str(every_object['pafy'].title)
            temp_details['author'] = str(every_object['pafy'].author)
            time = str(every_object['pafy'].duration).split(":")
            temp_details['duration'] = structure_time(seconds = int(time[2]),
                                                      minutes = int(time[1]),
                                                      hours = int(time[0])
                                                      )
            self.list_data.append(temp_details)
        return self.list_data

    def get_url_and_name(self,index):
        return [
                self.playlist['items'][int(index)]['pafy'].getbestaudio().url,
                self.playlist['items'][int(index)]['pafy'].title
                ]

    def get_next_index(self):
        try:
            assert isinstance(self.index, int), "invalid index"
        except AssertionError:
            self.index = 0
        if(self._random):
            self.next_index = randint(1, int(self.queue_len) - 1)
            return int(self.next_index)
        self.index = int(self.index)
        #repeat playlist
        if(self.repeat_mode == 3):
            if(self.index == self.queue_len - 1):
                self.next_index = 0
            else:
                self.next_index = self.index + 1
        #repeat single song
        elif(self.repeat_mode == 2):
            self.next_index = self.index
        #no repeat mode
        else:
            if(self.index == self.queue_len - 1):
                self.next_index = math.nan
            else:
                self.next_index = self.index + 1
        return self.next_index

    def get_prev_index(self):
        try:
            assert isinstance(self.index, int), "invalid index"
        except AssertionError:
            self.index = 0
        if(self.index <= 0):
            self.prev_index = math.nan
        else:
            self.prev_index = self.index - 1
        return self.prev_index

    def check_lock(self):
        self._lock_mutex.acquire()
        value = self._lock
        self._lock_mutex.release()
        return value

    def is_playing(self):
        if self.player.path:
            return True
        return False

    def toggle_lock(self, value):
        self._lock_mutex.acquire()
        self._lock = value
        self._lock_mutex.release()

    def play_at_index(self, index):
        self._song_changed = True
        self._new = False
        self.toggle_lock(True)
        self.index = index
        if math.isnan(self.index):
            pass
        #Play current index
        try:
            details = self.get_url_and_name(index)
        except:
            print("Couldn't fetch this song. Playing next.") #This needs to be in a new urwid error floating box. Will fix it later.
            self.play_next()
            return True
        url = details[0]
        self._currentSong = details[1]
        if(url==False):
            return False
        self.player.play(url)
        #Remove lock on continous_player
        while(not self.is_playing()):
            self.toggle_lock(True)
        self.toggle_lock(False)
        return True

    def stop(self):
        # This maybe removed in future, isn't really needed
        self.toggle_lock(True)
        # self.player.stop()

    def get_playlist_name(self):
        return self.playlist['title']

    def get_time_details(self):
        if self.player.duration:
            try:
                total_seconds = round(self.player.duration)
            except:
                print("Couldn't fetch this song. Playing next.") #This needs to be in a new urwid error floating box. Will fix it later.
                self.play_next()
        else:
            total_seconds = 0
        minutes = int(total_seconds / 60)
        seconds = total_seconds % 60
        self.time_details['total_time'] = structure_time_len(seconds, minutes)
        if self.player.playback_time:
            cur_seconds = round(self.player.playback_time)
        else:
            cur_seconds = 0
        minutes = int(cur_seconds / 60)
        seconds = cur_seconds % 60
        self.time_details['cur_time'] = structure_time_len(seconds, minutes)

        if(total_seconds is not 0):
            self.time_details['percentage'] = ( cur_seconds / total_seconds
                                              ) * 100
        else:
            self.time_details['percentage'] = 0
        return self.time_details

    def start_playing(self):
        if not self.player:
            self.player = mpv.MPV()
        thread = threading.Thread(target = self.continous_player, args={})
        thread.daemon = True
        thread.start()

    def continous_player(self):
        while(True):
            time.sleep(2)
            if(self.check_togglerLock()):
                continue
            if(self.is_playing() == False and self.check_lock() == False):
                self.toggle_lock(True)
                if(self._new):
                    self._new = False
                    self.index = 0
                    self.play_at_index(0)
                else:
                    _next = self.get_next_index()
                    if(math.isnan(_next)):
                        self.stop()
                    else:
                        self.play_at_index(int(_next))
                self._song_changed = True

    def play_next(self):
        self.stop()
        _next_index = self.get_next_index()
        if(not _next_index):
            return False
        self.play_at_index(_next_index)

    def play_prev(self):
        self.stop()
        _prev_index = self.get_prev_index()
        if(math.isnan(_prev_index)):
            # print("nothing previous here")
            return False
        self.play_at_index(_prev_index)

    def current_song_name(self):
        return self._currentSong

    def check_togglerLock(self):
        self._lock_mutex.acquire()
        value = self._togglerLock
        self._lock_mutex.release()
        return value

    def toggle_togglerLock(self, value):
        self._lock_mutex.acquire()
        self._togglerLock = value
        self._lock_mutex.release()

    def toggle_playing(self):
        if (self.player.pause):
            self.toggle_togglerLock(False)
            self.player.pause = False
        else:
            self.toggle_togglerLock(True)
            self.player.pause = True

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        assert(0 < volume < 100)
        self.volume = volume
        self.player['volume'] = volume
        return True

    def volume_up(self):
        volume = min(self.get_volume() + 10, 100)
        self.set_volume(volume)
        return True

    def volume_down(self):
        volume = max(self.get_volume() - 10, 0)
        self.set_volume(volume)
        return True
