import vlc

def entraMusik():
    return input("Código da Música: ")

def playMusik(player, Instance, nomeMusik):
    Media = Instance.media_new(nomeMusik + ".mp4")
    player.set_media(Media)
    player.set_fullscreen(True)
    player.play()

def stopMusik(player):
    player.stop()

def main():
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    while True:
        musik = entraMusik()
        playMusik(player,Instance,musik)
        input("Press Enter to Select Music.")
        stopMusik(player)
    

if __name__ == "__main__":
    main()
