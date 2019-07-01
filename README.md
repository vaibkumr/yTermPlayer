# ytTerm player (BETA)
Play youtube playlists as audio on linux terminal

[![Build Status](https://travis-ci.com/SamSamhuns/yTermPlayer.svg?branch=master)](https://travis-ci.com/SamSamhuns/yTermPlayer)
[![PyPI version](https://badge.fury.io/py/yTermPlayer.svg)](https://badge.fury.io/py/yTermPlayer)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/yTermPlayer.svg)](https://pypi.python.org/pypi/yTermPlayer/)
[![PyPI license](https://img.shields.io/pypi/l/yTermPlayer.svg)](https://pypi.python.org/pypi/yTermPlayer/)

## About
ytTerm player is a terminal youtube music player. It's completely written in python.

**UI**: Made using a wrapper for curses called [urwid][urwid]

**Player**: Handled using [python-mpv](https://github.com/jaseg/python-mpv)

**Stream fetch**: Audio streams from youtube are fetched using [pafy][pafy]

Features:
- Import and play youtube playlists on terminal
- Save playlists in library
- Use several playback modes such as repeat one, repeat list, random
- Download complete list (coming soon)

### Installation

Set up a virtual environment and install the dependencies:
```sh
$ pip install -r requirements.txt
```

python3 pip :-
```sh
$ pip install ytermplayer
$ yterm
```

or Git clone :-
```sh
$ git clone https://github.com/TimeTraveller-San/yTermPlayer
$ cd yTermPlayer/yTermPlayer/
$ python __main__.py
```

### Dependencies

Python 3

ytTerm player uses a number of open source projects to work properly:

*   [urwid][urwid]
*   [python-mpv](https://github.com/jaseg/python-mpv)
*   [pafy][pafy]
*   python3
*   mpv player (sudo pacman -S mpv) or (sudo apt-get install mpv)

ytTerm player itself is open source. Feel free to modify and distribute the code

### KeyBindings

| Key   | Function                             |
| :---  | :---                                 |
| s     | save current list                    |
| enter | select option/play song at selection |
| n     | play next song                       |
| p     | play previous song                   |
| space | pause/play song                      |
| u     | volume up                            |
| d     | volume down                          |
| q     | quit                                 |
| 1     | playback mode: Repeat one            |
| 2     | playback mode: Repeat list           |
| 3     | playback mode: None                  |
| r     | playback mode: Random                |
more features coming soon


### Screenshots
### Working video:  <https://youtu.be/rQpO1qBmxlY>
### Working video 2: <https://youtu.be/bQrNtcIcHc0>
### Start  screen :
![Start Screem](https://i.imgur.com/rvVUmDP.png)
### The UI will automatically use your terminal colors.
![Blue](https://i.imgur.com/R8a0Zy5.png)
![Yellow](https://i.imgur.com/TrHKuQg.jpg)

   [urwid]: <https://github.com/urwid/urwid>
   [vlc]: <https://github.com/oaubert/python-vlc>
   [pafy]: <https://github.com/mps-youtube/pafy>

### FAQ
-   How to fix out of range/url not found errors?

YouTube keeps changing its structure so it's important you have installed the latest version of youtube-dl as follows:
` pip install --upgrade youtube_dl `

-   Where are my playlists stored and how to delete playlists?

Playlists are saved in `$HOME/.yTermPlayer/playlists` as plain text. You may delete or add new playlists directly here.

-   How to contact me?

**Email:** time.traveller.san@gmail.com
**Twitter:** <https://twitter.com/timetravellertt>


### Known Bugs
-   ~~Buggy / unexpected playback behavior~~
It was caused because of race conditions and absence of critical section among the threads. Fixed it using semaphores

-   ~~If some VLC error starts showing up on the screen, just resize the terminal and it will be gone~~
Completely removed VLC and replaced it with much more minimal and faster mpv player. Thank to [python-mpv by jaseg](https://github.com/jaseg/python-mpv)
