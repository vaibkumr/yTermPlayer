# ytTerm player [BETA]
Play youtube playlists as audio on linux terminal

# About
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
First install the dependencies:
```sh
$ pip install -r requirements.txt
```
or

```sh
$ pip install  pafy==0.5.4 python-dateutil==2.7.3 python-mpv==0.3.9 urwid==2.0.1 virtualenv==15.1.0 youtube-dl==2018.8.4
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

* [urwid][urwid]
* [python-mpv](https://github.com/jaseg/python-mpv)
* [pafy][pafy]
* python3
* mpv player (sudo pacman -S mpv) or (sudo apt-get install mpv)


ytTerm player itself is open source. Feel free to modify and distribute the code

### KeyBindings

| Key       | Function  |
|:------------- |:-------------|
| s | save current list     |
| enter     | select option/play song at selection |
| n      | play next song     |  
| p | play previous song      |  
| space | pause/play song      |  
| q | quit      |  
| 1 | playback mode: Repeat one    |  
| 2 | playback mode: Repeat list      |  
| 3 | playback mode: None      |  
| r | playback mode: Random      |
more features coming soon




### Screenshots
### Working video:  https://youtu.be/rQpO1qBmxlY
### Workking video 2: https://youtu.be/bQrNtcIcHc0
### Start  screen :
![Start Screem](https://i.imgur.com/rvVUmDP.png)
#### The UI will automatically use your terminal colors.
![Blue](https://i.imgur.com/R8a0Zy5.png)
![Yellow](https://i.imgur.com/TrHKuQg.jpg)

   [urwid]: <https://github.com/urwid/urwid>
   [vlc]: <https://github.com/oaubert/python-vlc>
   [pafy]: <https://github.com/mps-youtube/pafy>

### Known Bugs
- ~~Buggy / unexpected playback behavior~~
It was caused because of race conditions and absence of critical section among the threads. Fixed it using semaphores

- ~~If some VLC error starts showing up on the screen, just resize the terminal and it will be gone~~
Completely removed VLC and replaced it with much more minimal and faster mpv player
