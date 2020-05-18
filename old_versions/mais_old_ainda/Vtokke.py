import vlc
import pandas as pd

def entraMusik2(dt):
    cod = input("Código da Música: ")
    return dt[dt.code == int(cod)].iloc[0,1]
    

#def entraMusik():
#    return input("Código da Música: ")

def playMusik(player, Instance, nomeMusik):
    Media = Instance.media_new(nomeMusik + ".mp4")
    player.set_media(Media)
    player.set_fullscreen(True)
    player.play()

def stopMusik(player):
    player.stop()

def main():
    catal = pd.read_csv("catalogo.csv", delimiter =';')
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    while True:
        musik = entraMusik2(catal)
        playMusik(player,Instance,musik)
        input("Press Enter to Select Music.")
        stopMusik(player)
    

if __name__ == "__main__":
    main()
