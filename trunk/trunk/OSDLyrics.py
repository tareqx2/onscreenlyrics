import time
__author__="Sridhar Mane"
__date__ ="$12 Oct, 2010 12:45:30 PM$"

#import sys
import dbus
import gobject
#if __name__ == '__main__':
#     install _() func before importing dbus_support
#    from common import i18n
#if dbus_support.supported:
import dbus
import dbus.glib
import signal
from Display import Display
from Search import Search
from LyricParser import LyricParser

class OSDLyrics:
    def __init__(self):
        print "\n*** OSDLyrics Initializing ***\n"
        self.bus = dbus.SessionBus()
        # setup dbus hooks
        remote_object_shell = self.bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Shell')
        self.iface_shell = dbus.Interface(remote_object_shell, 'org.gnome.Rhythmbox.Shell')
        remote_object_player = self.bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player')
        self.iface_player = dbus.Interface(remote_object_player, 'org.gnome.Rhythmbox.Player')
        print "\n*** OSDLyrics Initialized ***\n"

    def getCurrentTrackPosition(self):
        current_seconds = int(self.iface_player.getElapsed())
        current_position = str(int(current_seconds/60%60)).rjust(1,"0")+":"+str(int(current_seconds%60)).rjust(2,"0")
        return current_position

    def getCurrentTrackDetails(self):
        uri = self.iface_player.getPlayingUri()
        props = self.iface_shell.getSongProperties(uri)
        return props

class MusicTrackInfo(object):
    __slots__ = ['title', 'album', 'artist', 'duration', 'track_number', 'paused']

class MusicTrackListener(gobject.GObject):
    __gsignals__ = { 'music-track-changed': (gobject.SIGNAL_RUN_LAST, None, (object,)), }
    _instance = None
    @classmethod

    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        super(MusicTrackListener, self).__init__()
        self._last_playing_music = None
        self.bus = dbus.SessionBus()
        ## Rhythmbox
        self.bus.add_signal_receiver(self._player_name_owner_changed, 'NameOwnerChanged', 'org.freedesktop.DBus', arg0='org.gnome.Rhythmbox')
        self.bus.add_signal_receiver(self._rhythmbox_playing_changed_cb, 'playingChanged', 'org.gnome.Rhythmbox.Player')
        self.bus.add_signal_receiver(self._player_playing_song_property_changed_cb, 'playingSongPropertyChanged', 'org.gnome.Rhythmbox.Player')
        
    def _player_name_owner_changed(self, name, old, new):
        if not new: self.emit('music-track-changed', None)

    def _player_playing_changed_cb(self, playing):
        if playing:
            self.emit('music-track-changed', self._last_playing_music)
        else:
            self.emit('music-track-changed', None)

    def _player_playing_song_property_changed_cb(self, a, b, c, d):
        if b == 'rb:stream-song-title':
            self.emit('music-track-changed', self._last_playing_music)

    def _rhythmbox_playing_changed_cb(self, playing):
        if playing:
            info = self.get_playing_track()
            self.emit('music-track-changed', info)
        else:
            self.emit('music-track-changed', None)

    def _rhythmbox_properties_extract(self, props):
        info = MusicTrackInfo()
        info.title = props.get('title', None)
        info.album = props.get('album', None)
        info.artist = props.get('artist', None)
        info.duration = int(props.get('duration', 0))
        info.track_number = int(props.get('track-number', 0))
        return info

    def get_playing_track(self):
        ## Check Rhythmbox
        test = False
        if hasattr(self.bus, 'name_has_owner'):
            if self.bus.name_has_owner('org.gnome.Rhythmbox'):
                test = True
        elif dbus.dbus_bindings.bus_name_has_owner(self.bus.get_connection(),'org.gnome.Rhythmbox'):
            test = True
            if test:
                rbshellobj = self.bus.get_object('org.gnome.Rhythmbox','/org/gnome/Rhythmbox/Shell')
                player = dbus.Interface(self.bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player'), 'org.gnome.Rhythmbox.Player')
                rbshell = dbus.Interface(rbshellobj, 'org.gnome.Rhythmbox.Shell')
                try:
                    uri = player.getPlayingUri()
                except dbus.DBusException:
                    uri = None
                if not uri:
                    return None
                props = rbshell.getSongProperties(uri)
                info = self._rhythmbox_properties_extract(props)
                self._last_playing_music = info
                return info

def main():
#    osdlyr = OSDLyrics()
    mtl = MusicTrackListener()
#    dis_pre = Display("pre")
#    dis_live = Display("live")
#    search = Search()
#    parser = LyricParser()
    def music_track_change_cb(listener, music_track_info):
        print music_track_info
        print listener
#        props = osdlyr.getCurrentTrackDetails()
#        info = mtl._rhythmbox_properties_extract(props)
#        dis_pre.display("Now Playing")
#        dis_live.display("[ Title ]: "+info.title+" [Artist]: "+info.artist)
#        duration = str(int(info.duration/60%60)).rjust(2,"0")+":"+str(int(info.duration%60)).rjust(2,"0")
#        fileURI=search.searchLocalDirectory(info)
#        if fileURI is not None:
#            print fileURI
#            parser.parseLyricFile(fileURI)
#	    if fileURI :
#                status ="START"
#                while status != "END":
#                    time.sleep(1)
#                    line = parser.getNowPlayingLine(duration,fileURI)
#                    if line is not "~" :
#                            if line == "END" :
#                                    break
##                            elif line == "" :
##                                    break
#                            else :
#                                    dis_live.display(line)



#            def local(osdlyr,dis):
#            current_pos=osdlyr.getCurrentTrackPosition()
#            dis.display(parser.getNowPlayingLine(current_pos))
#            t=Timer(1.0,local(osdlyr,dis))
#            t.start()
#    listener = MusicTrackListener.get()
    mtl.connect('music-track-changed', music_track_change_cb)
#    track = listener.get_playing_track()
#
#    if track is None:
#        print 'Now not playing anything'
#    else:
#        print 'Now playing: "%s" by %s' % (track.title, track.artist)
    gobject.MainLoop().run()


if __name__ == '__main__':
    main()
