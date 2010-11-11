__author__="Sridhar Mane"
__date__ ="$14 Oct, 2010 7:42:01 PM$"
from fileinput import close
import dbus
class LyricParser:
    def __init__(self):
        self.lyricsDict = dict()
        self.bus = dbus.SessionBus()
        remote_object_player = self.bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player')
        self.iface_player = dbus.Interface(remote_object_player, 'org.gnome.Rhythmbox.Player')
	self.fileURI = None

    def parseLyricFile(self,fileURI):
	self.fileURI=fileURI
        file = open(fileURI)
        for line in file:
            time=line.split("]")[0].strip("[").split(".")[0]
            if len(line.split("]")) > 1 :
                sentence=line.split("]")[1].strip()
            else:
                sentence=""
            self.lyricsDict[time] = sentence
        close()
        #return self.lyricsDict

    def getNowPlayingLine(self,duration,fileURI):
        if self.fileURI == fileURI :
            time = self.getCurrentTrackPosition()
            if time < duration:
                if time in self.lyricsDict :
                    return self.lyricsDict[time]
                else :
                    return "~"
            else :
              return "END"
        else :
            self.parseLyricFile(self.fileURI)
            
    def getCurrentTrackPosition(self):
	try :
        	current_seconds = int(self.iface_player.getElapsed())
        	current_position = str(int(current_seconds/60%60)).rjust(2,"0")+":"+str(int(current_seconds%60)).rjust(2,"0")
        	return current_position
	except DBusException:
		return "99:99"
