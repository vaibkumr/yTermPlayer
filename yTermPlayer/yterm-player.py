#!/usr/bin/env python3
'''
yTermPlayer by TimeTraveller
(https://github.com/TimeTraveller-San/yTermPlayer)
Special thanks for these libraries and their contributors:
- urwid
- pafy
- python-mpv
'''

from .music_api import YoutubePlayer
from .ui import player_ui
from .settings import PL_DIR
import os
import urwid

palette = [
    ('reversed', 'standout', ''),
    ('b', 'black', 'dark gray'),
    ('highlight', 'black', 'light blue'),
    ('bg', 'black', 'dark blue'),]
if __name__ == "__main__":
    new_player = player_ui()
    loop = urwid.MainLoop(
                        new_player.draw_ui(),
                        palette,
                        unhandled_input = new_player.handle_keys
                        )
    loop.set_alarm_in(2, new_player.update_name)
    loop.run()
