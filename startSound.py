from classes.Audio import audio

audio = audio

mode = 0
volume = 100

with open("./database/mode.txt", "r") as modeFile:
    modeLine = modeFile.readline()
    if isinstance(modeLine, str):
        if modeLine != "":
            mode = int(modeLine)

with open("./database/sound-volume.txt", "r") as volumeFile:
    volumeLine = volumeFile.readline()
    if isinstance(volumeLine, str):
        volumeFile.seek(0)
        if volumeLine != "":
            volumeFile.seek(0)
            volume = int(volumeLine)

if mode == 1:
    audio.play_audio("audio/systemAudio/start-mode-expert.ogg", volume)
if mode == 2:
    audio.play_audio("audio/systemAudio/start-mode-intermediary.ogg", volume)
if mode == 3:
    audio.play_audio("audio/systemAudio/start-mode-tutorial.ogg", volume)

