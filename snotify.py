#! /usr/bin/env python
# coding: utf8
import wnck, gtk, gobject
import pynotify
import subprocess

def mute():
    p = subprocess.Popen('echo set-sink-mute 0 1 | pacmd > /dev/null', shell=True)
def unmute():
    p = subprocess.Popen('echo set-sink-mute 0 0 | pacmd > /dev/null', shell=True)

s = wnck.screen_get_default()
connected = False
commercials = ["mount forever", "bilfri", "this city" , "kanal 5", "spotify - spotify", "rosa bandet",
"share my playlists", "warner music", "landsting", "meet n greet", "universal music", "lion alpin",
"svenska spel", "sony pictures", "emi sweden", "sony pictures", "sony music", "activision", "virgin/emi"]

pynotify.init("Spotify notification test")

def is_commercial(text):
    for comm_text in commercials:
        if comm_text in text.lower():
            return True
    return False

def name_changed(window):
    name = window.get_name()
    print "Name changed:", name;
    chunks = name.split("-")
    commercial = False
    if name.lower().strip(" -") == "spotify":
        text = "Playback stopped"
    elif is_commercial(window.get_name()):
        text = "Reklamavbrott, vi beklagar"
        commercial = True
    else:
        text = "Now playing: " + name[10:]

    if commercial == True:
        mute()
    else:
        unmute()

    n = pynotify.Notification("Spotify", text)
    n.set_timeout(3000)
    n.show()
    print

def run():
    global connected
    ws = s.get_windows()
    print [w.get_name() for w in ws]
    print
    w = [w for w in ws if "Spotify" in w.get_name()][0]
    if not connected:
        print "Connecting:", w
        w.connect("name-changed", name_changed)
        connected = True

if __name__ == '__main__':
    gobject.idle_add(run)

    gtk.main()
