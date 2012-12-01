#  player_controls.py
#  Simple wrapper to iTunes' AppleScript interface
#  (see bottom of module for info)

import Foundation, objc;

NSAppleScript = objc.lookUpClass('NSAppleScript')

def run_script(cmd):
    script = NSAppleScript.alloc().initWithSource_(cmd)
    err = None
    ret = script.executeAndReturnError_(err)
    if not ret:
       print "Error: " + err + "\n"
    return ret

def play(track=None, playlist=None):
    cmd = 'tell application "iTunes" to play'
    if track:
      cmd += ' track "' + track + '"'
    elif playlist:
      cmd += ' playlist"' + playlist +'"'
    run_script(cmd)

def pause():
    cmd = 'tell application "iTunes" to pause'
    run_script(cmd)

def playpause():
    cmd = 'tell application "iTunes" to playpause'
    run_script(cmd)

def stop():
    cmd = 'tell application "iTunes" to stop'
    run_script(cmd)

def next_track():
    cmd = 'tell application "iTunes" to next track'
    run_script(cmd)

def back_track():
    cmd = 'tell application "iTunes" to back track'
    run_script(cmd)

def previous_track():
    cmd = 'tell application "iTunes" to previous track'
    run_script(cmd)

def get_playlists():
    cmd = 'tell application "iTunes" to get name of playlists'
    ret = run_script(cmd)
    c = ret[0].numberOfItems()
    if c > 0:
        playlists = []
        x = 0
        while x <= c:
            playlist = None
            try:
               playlist = ret[0].descriptorAtIndex_(x).stringValue()
            except:
               pass
            if playlist:
                playlists.append(playlist)
            x += 1
        return playlists
    else:
        return None

def get_playlist_tracks(playlist):
    cmd = 'tell application "iTunes" to get name of tracks in playlist "' + playlist + '"'
    ret = run_script(cmd)
    c = ret[0].numberOfItems()
    if c > 0:
        tracks = []
        x = 0
        while x <= c:
            track = None
            artist = None
            length = None
            try:
                track = ret[0].descriptorAtIndex_(x).stringValue()
                artist = run_script('tell application "iTunes" to get artist of track "' + track + '"')[0].stringValue()
                album = run_script('tell application "iTunes" to get album of track "' + track + '"')[0].stringValue()
                length = run_script('tell application "iTunes" to get time of track "' + track + '"')[0].stringValue()
            except:
                pass
            if track:
                tracks.append([artist, track, album, length])
            x += 1
        return tracks
    else:
        return None

def get_current_track():
    track = None
    artist = None
    album = None
    try:
        track = run_script('tell application "iTunes" to get name of current track')[0].stringValue()
        artist = run_script('tell application "iTunes" to get artist of current track')[0].stringValue()
        album = run_script('tell application "iTunes" to get album of current track')[0].stringValue()
    except:
        pass
    return [artist, track, album]

def get_player_position():
    t = run_script('tell application "iTunes" to get time of current track')[0]
    if not t:
        return 0
    t = t.stringValue()
    m, s = t.split(':')
    m = int(m)
    s = int(s)
    pos = run_script('tell application "iTunes" to get player position')[0].int32Value()
    return (pos*100)/((m * 60) + s)

def set_player_position(p):
    t = run_script('tell application "iTunes" to get time of current track')[0]
    if not t:
        return 0
    t = t.stringValue()
    m, s = t.split(':')
    m = int(m)
    s = int(s)
    pos = (p*((m * 60) + s))/100
    run_script('tell application "iTunes" to set player position to %d' % pos)[0].int32Value()

def is_playing():
    cmd = 'tell application "iTunes" to get player state'
    ret = False
    try:
        ret = run_script(cmd)[0].stringValue() == 'kPSP'
    except:
        pass
    return ret

def hide_itunes():
    cmd = 'tell application "iTunes" to close windows'
    run_script(cmd)

# Volume controls
def set_volume_percent(p=50):
    cmd = 'tell application "iTunes" to set the sound volume to %d' % p
    run_script(cmd)

def get_volume_percent():
    cmd = 'tell application "iTunes" to get the sound volume'
    return run_script(cmd)[0].int32Value()

# TODO: Equalizer controls

"""
player_controls.py

- Super simple Python wrapper to the iTunes player's Applescript interface

Just import this module in your project and call the modules. E.g. To play the current playlist,

import player_controls
player_controls.play()

As easy as that.

Copyright (c) 2012 Moises Anthony Aranas

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
