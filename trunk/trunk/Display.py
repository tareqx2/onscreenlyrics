
__author__="Sridhar Mane"
__date__ ="$12 Oct, 2010 12:57:52 PM$"

class Display:
    def __init__(self,state):
        import pyosd
        if state == "pre" :
            osdfont = "-*-helvetica-medium-r-normal-*-*-200-*-*-p-*-iso8859-1"
            self.pyosd=pyosd.osd(font=osdfont, colour="green", timeout=3, pos=1, offset=100, hoffset=0, shadow=1, align=1, lines=2, noLocale=False)
            self.pyosd.wait_until_no_display()
        elif state == "live" :
            osdfont = "-*-helvetica-medium-r-normal-*-*-230-*-*-p-*-iso8859-1"
            self.pyosd=pyosd.osd(font=osdfont, colour="maroon", timeout=3, pos=1, offset=50, hoffset=0, shadow=1, align=1, lines=2, noLocale=False)
            self.pyosd.wait_until_no_display()
    def display(self,message):
        self.pyosd.display(message)
