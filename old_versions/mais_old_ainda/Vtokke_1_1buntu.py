#! /usr/bin/python
# -*- coding: utf-8 -*-

#
# tkinter example for VLC Python bindings
# Copyright (C) 2015 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#
"""A simple example for VLC python bindings using tkinter. Uses python 3.4

Author: Patrick Fay
Date: 23-09-2015
"""

# import external libraries
import vlc
import sys
import pandas as pd

if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename

# import standard libraries
import os
import pathlib
from threading import Thread, Event
import time
import platform

dt = pd.read_csv("catalogo.csv", delimiter =',', encoding = 'utf-8')
print(dt)
dt["code"] = pd.to_numeric(dt["code"])
fila = pd.DataFrame(columns=['codigo'])


class Player(Tk.Frame):
    """The main window has to deal with events.
    """
        
    def __init__(self, parent, title=None):
        global fila
        Tk.Frame.__init__(self, parent)
        self.parent = parent

        if title == None:
            title = "tk_vlc"
        self.parent.title(title)

        # The second panel holds controls
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)

        ctrlpanel = ttk.Frame(self.parent)
        lab = ttk.Label(ctrlpanel, text="Codigo Musica: ")
        lab1 = ttk.Label(ctrlpanel, text="Proxima Musica: ")
        codigo = ttk.Entry(ctrlpanel)
        codigo.focus_force()
        lab.pack(side=Tk.LEFT)
        codigo.pack(side=Tk.LEFT)
        lab1.pack(side=Tk.LEFT)
        ctrlpanel.pack(side=Tk.BOTTOM)
        ctrlpanel2 = ttk.Frame(self.parent)
        self.scale_var = Tk.DoubleVar()
        ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)

        def addList(btn):
            global fila
            # if a file is already running, then stop it.
            if codigo.get() != '':
                if (any(dt.code == int(codigo.get()))):
                    print(dt[dt.code == int(codigo.get())])
                    fila = fila.append({ 'codigo' : int(codigo.get())} , ignore_index=True)
                    print(fila)
                    if len(fila.index)== 1:
                        lab1.configure(text = "Proxima Musica - " + dt[dt.code == fila.iloc[0,0]].iloc[0,3] + " - " + dt[dt.code == fila.iloc[0,0]].iloc[0,2])
                else:
                    print("Musica nao esta no catalogo")
            codigo.delete(0,'end')
                
                
        def onopen(btn):
            global fila
            # if a file is already running, then stop it.
            self.player.stop()
            print(fila)
            title = dt[dt.code == fila.iloc[0,0]].iloc[0,1]
            fila = fila.iloc[1:]
            if len(fila.index)>= 1:
                lab1.configure(text = "Proxima Musica - " + dt[dt.code == fila.iloc[0,0]].iloc[0,3] + " - " + dt[dt.code == fila.iloc[0,0]].iloc[0,2])
            else:
                lab1.configure(text = "Proxima Musica: Nenhuma")
            if os.path.exists("./musicas/" + title):
                Media = self.Instance.media_new("./musicas/" + title)
                self.player.set_media(Media)
                if platform.system() == 'Windows':
                    self.player.set_hwnd(self.GetHandle())
                else:
                    self.player.set_xwindow(self.GetHandle()) # this line messes up windows
                self.player.play()
            else:
                print("Musica no catalogo porem arquivo .mp4 nao encontrado")

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        codigo.bind('<Return>', addList)
        codigo.bind('<Tab>', onopen)

        # below is a test, now use the File->Open file menu
        #media = self.Instance.media_new('output.mp4')
        #self.player.set_media(media)
        #self.player.play() # hit the player button
        #self.player.video_set_deinterlace(str_to_bytes('yadif'))

        #self.player.set_hwnd(self.GetHandle()) # for windows, OnOpen does does this
    
    def GetHandle(self):
        return self.videopanel.winfo_id()


    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        Tk.tkMessageBox.showerror(self, 'Error', errormessage)

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"): #(1)
        Tk_get_root.root= Tk.Tk()  #initialization call is inside the function
    return Tk_get_root.root

def _quit(self):
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    os._exit(1)

if __name__ == "__main__":
    # Create a Tk.App(), which handles the windowing system event loop
    root = Tk_get_root()
    root.bind('<F4>', _quit)
    root.attributes("-fullscreen", True)
    player = Player(root)
    # show the player window centred and run the application
    root.mainloop()
