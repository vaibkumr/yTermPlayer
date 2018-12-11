import os
import platform

HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
MODULE_DIR = os.path.dirname(__file__)
PL_DIR = os.path.join(HOME, ".yTermPlayer", "playlists")
OS = platform.uname()[0]
