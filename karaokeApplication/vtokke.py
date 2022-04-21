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
from subprocess import check_output
import tkinter as Tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

# import standard libraries
import os
import pathlib
from threading import Thread, Event
import time
import platform
import guigolock as ggl

current_location = os.path.dirname(os.path.abspath(__file__)) + '/'

df = pd.read_csv(current_location + "catalogo.csv", delimiter =',', encoding = 'utf-8', dtype=str)
if os.path.exists("catalogo_custom.csv"):
    dfc = pd.read_csv("catalogo_custom.csv", delimiter =',', encoding = 'utf-8', dtype=str)
    dt = pd.concat([df, dfc])
else:
    dt = df
dt["code"] = pd.to_numeric(dt["code"])
pd.DataFrame(columns=['codigo', 'nome','artista', 'responsavel']).to_csv('./filomena')


class Player(Tk.Frame):
    """The main window has to deal with events.
    """
        
    def __init__(self, parent, title=None):
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
        lab = ttk.Label(ctrlpanel, text=" Codigo Musica: ")
        lab1 = ttk.Label(ctrlpanel, text="Proxima Musica: ")
        if os.name == "nt":
            lab3 = ttk.Label(ctrlpanel, text=check_output('ipconfig | find "IPv4"', shell = True).split()[-1])
        else:
            lab3 = ttk.Label(ctrlpanel, text=check_output(['hostname', '--all-ip-addresses']).split()[0])
        codigo = ttk.Entry(ctrlpanel)
        codigo.focus_force()
        lab3.pack(side=Tk.LEFT)
        lab.pack(side=Tk.LEFT)
        codigo.pack(side=Tk.LEFT)
        lab1.pack(side=Tk.LEFT)
        ctrlpanel.pack(side=Tk.BOTTOM)
        ctrlpanel2 = ttk.Frame(self.parent)
        self.scale_var = Tk.DoubleVar()
        ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)

        def addList(btn):
            global dt
            # if a file is already running, then stop it.
            if codigo.get() != '':
                df = pd.read_csv(current_location + "catalogo.csv", delimiter =',', encoding = 'utf-8', dtype=str)
                if os.path.exists("catalogo_custom.csv"):
                    dfc = pd.read_csv("catalogo_custom.csv", delimiter =',', encoding = 'utf-8', dtype=str)
                    dt = pd.concat([df, dfc])
                else:
                    dt = df
                dt["code"] = pd.to_numeric(dt["code"])
                if (any(dt.code == int(codigo.get()))):
                    print(dt[dt.code == int(codigo.get())])
                    while ggl.check_free('./filomena', 'vtk') != True:
                        print('filomena presa')
                    fila = pd.read_csv('./filomena')
                    fila = fila.append({'codigo':codigo.get(),'nome':dt[dt.code == int(codigo.get())].iloc[0,3],'artista': dt[dt.code == int(codigo.get())].iloc[0,2], 'responsavel':'vtk'}, ignore_index=True)
                    fila.to_csv('./filomena')
                    while ggl.release('./filomena', 'vtk') != True:
                        print('incapaz de liberar filomena')
                    print(fila)
                    if len(fila.index)== 1:
                        lab1.configure(text = "Proxima Musica - " + fila['nome'].iloc[0] + " - " + fila['artista'].iloc[0])
                else:
                    print("Musica nao esta no catalogo")
            codigo.delete(0,'end')
                
                
        def onopen(btn):
            # if a file is already running, then stop it.
            self.player.stop()
            while ggl.check_free('./filomena', 'vtk') != True:
                print('filomena presa')
            fila = pd.read_csv('./filomena')
            frst = fila.iloc[0]
            fila = fila.iloc[1:]
            fila = fila.reset_index(drop=True)
            fila.to_csv('./filomena')
            while ggl.release('./filomena', 'vtk') != True:
                print('incapaz de liberar filomena')
            print(fila)
            if len(fila.index) > 1:
                lab1.configure(text = "Proxima Musica - " + fila['nome'].iloc[0] + " - " + fila['artista'].iloc[0])
            elif len(fila.index) == 1:
                lab1.configure(text = "Proxima Musica - " + fila['nome'] + " - " + fila['artista'])
            else:
                lab1.configure(text = "Proxima Musica: Nenhuma")
            if os.path.exists("/media/pi/Elements/karaoke/musicas/" + str(frst['codigo']).zfill(5) + '.mp4'):
                Media = self.Instance.media_new("/media/pi/Elements/karaoke/musicas/" + str(frst['codigo']).zfill(5) + '.mp4')
                self.player.set_media(Media)
                if platform.system() == 'Windows':
                    self.player.set_hwnd(self.GetHandle())
                else:
                    self.player.set_xwindow(self.GetHandle()) # this line messes up windows
                self.player.play()
            elif os.path.exists("./musicas/" + str(frst['codigo']).zfill(5) + '.mp4'):
                Media = self.Instance.media_new("./musicas/" + str(frst['codigo']).zfill(5) + '.mp4')
                self.player.set_media(Media)
                if platform.system() == 'Windows':
                    self.player.set_hwnd(self.GetHandle())
                else:
                    self.player.set_xwindow(self.GetHandle())  # this line messes up windows
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
