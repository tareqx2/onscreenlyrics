__author__="Sridhar Mane"
__date__ ="$14 Oct, 2010 2:15:21 AM$"
import os
import re
class Search:
    def __init__(self):
        self.lyricdir = "/home/mane/Documents/lyrics"
        self.fileURI=""

    def searchLocalDirectory(self,info):
        list = os.listdir(self.lyricdir)
        if list:
            for name in list:
                fileInfo=name.split("-")
                if fileInfo[0].lower().strip() == info.artist.lower():
                    if fileInfo[1].split(".")[0].lower().strip() == info.title.lower():
                        self.fileURI=name
                        return self.lyricdir+"/"+self.fileURI

        else:
            print "No Lyric Found : Searching Online"
            #No Lyrics found, so search on server and download
            self.searchServer(info)
    
    def searchServer(self,info):

        return file
