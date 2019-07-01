#!/usr/bin/env python3
'''
yTermPlayer GUI by TimeTraveller
(https://github.com/TimeTraveller-San/yTermPlayer)
Sorry for no comments and not following PEP 8 styling guide, fixing it soon.
Special thanks for these libraries and their contributors:
- urwid
- pafy
- python-mpv
'''
import urwid
import time, os, sys
from .music_api import YoutubePlayer

LIST_LOCK = True

class my_bar(urwid.ProgressBar):
    def get_text(self):
            return ""

palette = [
    ('reversed', 'standout', ''),
    ('b', 'black', 'dark gray'),
    ('highlight', 'black', 'light blue'),
    ('bg', 'black', 'dark blue'),]

class player_ui(YoutubePlayer):
    def __init__(self):
        self._list_updated = False #Update this variable as True only when a new list has been initlaized
        self.current_marked_index =- 1 #To highlight currently playing song
        self.player_object = YoutubePlayer()
        self._isplayerUI = False
        self._play_pause_lock = False
        self.top = self.start_screen()

    def update_name(self,_loop, _data):
        global LIST_LOCK
        # Update list
        if(self._list_updated):
            _new_list=[]
            heading = urwid.Columns([(6,urwid.Text(u"Track",align='left')),
                                    (15,urwid.Text(u"Duration",align='left')),
                                    urwid.Text(u"Title",align='left'),
                                    urwid.Text(u"Artist",align='left')],
                                    dividechars=0, focus_column=None,
                                    min_width=1, box_columns=None
                                    )
            _list_data=self.player_object.get_list_data()
            track_no=1 #Increament this in loop
            for _item in _list_data:
                _new_list.append(urwid.AttrMap(urwid.Columns(
                    [
                    (6,urwid.Text(str(track_no), align = 'left')),
                    (15,my_Text(_item["duration"], align = 'left')),
                    my_Text(_item["title"], align='left'),
                    my_Text(_item["author"], align='left')
                    ],
                    dividechars = 0, focus_column = None, min_width = 1,
                    box_columns = None),
                    None,focus_map = 'reversed'))
                track_no = track_no + 1
            self.list[:] = _new_list
            self.playlistbox.set_focus(0, coming_from=None)
            self._list_updated=False
        #Update player second by second things
        if(self._isplayerUI):
            if(not self._play_pause_lock):
                self.txt2_2.set_text("Playing: " +
                                    str(self.player_object.current_song_name())
                                    )
            temp = self.player_object.get_time_details()
            self.pb.set_completion(temp['percentage'])
            self.txt2_1.set_text(str(temp['cur_time']
                                + "/"
                                +str(temp['total_time']))
                                )
            self.pb_text.set_text(str(temp['cur_time']
                                + "/"
                                +str(temp['total_time']))
                                )
            #Unmark previous
            if(self.current_marked_index is not -1):
                self.list[self.current_marked_index].set_attr_map({
                                                                'highlight':None
                                                                })
            #Mark new
            self.list[int(self.player_object.get_index())].set_attr_map({
                                                                None:'highlight'
                                                                })
            self.current_marked_index=int(self.player_object.get_index())
        #Change focus of liswalker dynamically
        if(self.player_object._song_changed):
            self.playlistbox.set_focus(self.player_object.get_index(),
                                       coming_from=None)
            self.player_object._song_changed = False
        #if no global list lock, it means enter has been pressed
        if(not LIST_LOCK):
            #PLay the song at highlight
            LIST_LOCK = True
            self.player_object.stop()
            self.player_object.play_at_index(int(self.playlistbox.focus_position))
        #Reset alarm within 1 second to update further data
        _loop.set_alarm_in(0.1, self.update_name)

    def draw_ui(self):
        #Draws the start UI
        self.bottom = self.make_player_ui()
        self.top = self.start_screen()
        self.ui_object = urwid.Padding(urwid.Overlay(self.top, self.bottom,
                                    'center', 50,
                                    'middle', 20,
                                    min_width=None,
                                    min_height=None, left=0, right=0,
                                    top=0, bottom=0),
                                    right=0, left=0
                                    )
        return self.ui_object

    def make_player_ui(self):
        #Draws the main player UI
        #Header
        self.txt2_1 = urwid.Text("--/--",align='left')
        self.txt2_2 = urwid.Text("Playing: None",align='center')
        self.txt2_3 = urwid.Text(u"Mode: Repeat off",align='right')
        cols=urwid.Columns(
                            [self.txt2_1, self.txt2_2, self.txt2_3],
                            dividechars=0, focus_column=None,
                            min_width=1, box_columns=None
                            )
        head_widget=urwid.Pile([cols],focus_item=None)
        head_final_widget=self.body=urwid.LineBox(
                        head_widget, title='Terminal Youtube Player',
                        title_align='center', tlcorner='┌', tline='─',
                        lline='│', trcorner='┐',blcorner='└',
                        rline='│', bline='─', brcorner='┘'
                        )
        #body
        self.list = urwid.SimpleFocusListWalker([])
        heading=urwid.Columns(
                        [(6,urwid.Text(u"Track",align='left')),
                        (15,urwid.Text(u"Duration",align='left')),
                        urwid.Text(u"Title",align='left'),urwid.Text(
                        u"Artist",align='left')], dividechars=0,
                        focus_column=None, min_width=1, box_columns=None
                        )
        self.playlistbox = urwid.ListBox(self.list)
        self.body_pile = urwid.Pile(
                        [(1,urwid.Filler(heading,valign='top', height='pack',
                        min_height=None, top=0, bottom=0)),
                        (1,urwid.Filler(urwid.Divider())),self.playlistbox],
                        focus_item=2
                        )
        self.body = urwid.LineBox(
                                self.body_pile, title="", title_align='center',
                                tlcorner='┌', tline='─', lline='│',
                                trcorner='┐', blcorner='└', rline='│',
                                bline='─', brcorner='┘'
                                )
        #Footer Progress bar
        self.pb = my_bar("reversed","highlight" )
        self.pb.set_completion(0)
        self.pb_text = urwid.Text("",align='right')
        footer_widget = urwid.Columns(
                                [self.pb,(14,self.pb_text)],dividechars=0,
                                focus_column=None, min_width=1,
                                box_columns=None
                                )
        #Final player_ui object
        player_ui_object = urwid.Frame(self.body, header=head_final_widget,
                                footer=footer_widget, focus_part='body')
        return urwid.Padding(player_ui_object,right=0,left=0)

    def start_screen(self):
        #Ovrlay top screen at start
        txt1_1=urwid.Button("New playlist [Enter URL]")
        urwid.connect_signal(txt1_1, 'click', self.input_screen)
        txt1 = urwid.AttrMap(txt1_1,None,focus_map='reversed')
        txt2_2=urwid.Button("Load saved playlist")
        urwid.connect_signal(txt2_2, 'click', self.load_list_screen)
        txt2 = urwid.AttrMap(txt2_2,None,focus_map='reversed')
        start_list=urwid.SimpleFocusListWalker([txt1,txt2])
        box=urwid.ListBox(start_list)
        selection=urwid.LineBox(
                                box, title='', title_align='center',
                                tlcorner='┌', tline='─', lline='│',
                                trcorner='┐', blcorner='└', rline='│',
                                bline='─', brcorner='┘'
                                )
        selection_with_padding=urwid.Padding(selection,left=2,right=2)
        return selection_with_padding

    def input_screen(self,button):
        #overlay second screen after start case1
        txt=urwid.Text("Enter the URL below: ")
        url_field=urwid.Edit(caption='', edit_text='', multiline=False,
                            align='left', wrap='space', allow_tab=False,
                            edit_pos=None, layout=None, mask=None)
        btn=urwid.Button("OK",user_data=None)
        url_button = urwid.AttrMap(btn,None,focus_map='reversed')
        urwid.connect_signal(btn, 'click', self.input_url,url_field)
        wid=urwid.Pile([txt,url_field,url_button])
        new=urwid.Filler(urwid.AttrMap(wid, None, focus_map=''))
        ok_screen_box=urwid.LineBox(
                                    new, title='', title_align='center',
                                    tlcorner='┌', tline='─', lline='│',
                                    trcorner='┐', blcorner='└', rline='│',
                                    bline='─', brcorner='┘'
                                    )
        self.top.original_widget=ok_screen_box

    def load_list_screen(self,button):
        #overlay second screen after start case2
        txt=urwid.Text("Choose from the following:- ")
        _list=self.player_object.get_saved_lists()
        saved_list=[]
        for every_list in _list:
            b=urwid.Button(str(every_list).rstrip(),user_data=None)
            urwid.connect_signal(b, 'click', self.list_load)
            saved_list.append(urwid.AttrMap(b,None,focus_map='reversed'))
        box=urwid.ListBox(urwid.SimpleFocusListWalker(saved_list))
        list_box=urwid.LineBox(
                                box, title='', title_align='center',
                                tlcorner='┌', tline='─', lline='│',
                                trcorner='┐', blcorner='└', rline='│',
                                bline='─', brcorner='┘'
                                )
        list_box_padding=urwid.Padding(list_box,right=0,left=0)
        self.top.original_widget=list_box_padding

    def list_load(self,button):
        self.player_object.load_saved_playlist(str(button.get_label()).rstrip())
        self.player_object.start_playing()
        self._list_updated=True
        self._isplayerUI=True
        self.ui_object.original_widget=self.make_player_ui()

    def input_url(self,button,url_field):
        url=url_field.get_edit_text().rstrip()
        self.init_list_and_listui(str(url))

    def init_list_and_listui(self,url):
        #New list has been loaded,remake the UI
        self.player_object.initPlaylist(url)
        self.player_object.start_playing()
        self._list_updated=True
        self._isplayerUI=True
        self.ui_object.original_widget=self.make_player_ui()

    #Utility functions down below
    def change_play_mode_to_repeat_one(self):
        self.txt2_3.set_text("Mode: Repeat one")
        self.player_object.set_repeat_mode(2)

    def change_play_mode_to_repeat_list(self):
        self.txt2_3.set_text("Mode: Repeat list")
        self.player_object.set_repeat_mode(3)

    def change_play_mode_to_repeat_off(self):
        self.txt2_3.set_text("Mode: Repeat off")
        self.player_object.set_repeat_mode(1)

    def change_play_mode_to_random(self):
        self.txt2_3.set_text("Mode: Random")
        self.player_object.play_random()

    def toggle_playing(self):
        if(self._play_pause_lock):
            self._play_pause_lock=False
        else:
            self._play_pause_lock=True
        self.player_object.toggle_playing()
        self.txt2_2.set_text("[PAUSED]: "
                            + str(self.player_object.current_song_name()))

    def volume_up(self):
        self.player_object.volume_up()

    def volume_down(self):
        self.player_object.volume_down()

    def save_list(self):

        self.player_object.save_current_list()

    def handle_keys(self,key):
        if(key=='q'):
            raise urwid.ExitMainLoop()
        key_dict={
        'n':self.player_object.play_next,
        'p':self.player_object.play_prev,
        ' ':self.toggle_playing,
        's':self.save_list,
        '1': self.change_play_mode_to_repeat_one,
        '2': self.change_play_mode_to_repeat_list,
        '3': self.change_play_mode_to_repeat_off,
        'r': self.change_play_mode_to_random,
        'u': self.volume_up,
        'd': self.volume_down,
        }
        try:
            key_dict[key]()
        except:
            pass

class my_Text(urwid.Text):
    def selectable(self):
        return True
    def keypress(self, size, key):
        global LIST_LOCK #CAN't FIND ANY OTHER WAY THAN THIS TO CHANGE THE VARIABLES OF MY player_ui CLASS
        if(key=='enter'):
            LIST_LOCK = False
        elif(key == 'q'):
            raise urwid.ExitMainLoop()
        return key


if __name__ == "__main__":
    new_player = player_ui()
    ui = new_player.draw_ui()
    loop = urwid.MainLoop(ui, palette, unhandled_input = new_player.handle_keys)
    loop.set_alarm_in(2, new_player.update_name)
    loop.run()
