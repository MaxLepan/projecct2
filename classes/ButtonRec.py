import os
from .Micro import Micro
from .Audio import Audio
from .AudioGetter import AudioGetter

class ButtonRec:
    volume = 100
    micro = Micro()
    

    def __init__(self) -> None:
        self.audio = Audio()
        self.messageRecorded = False

    def mode_1_rec(self, pattern):
        audioGet = AudioGetter(pattern)
        audioFile = audioGet.get_audio()
        if "noMessageRecorded" in audioFile:
            self.messageRecorded = False
            self.audio.play_audio("audio/systemAudio/soundChanged.ogg", ButtonRec.volume)
            ButtonRec.micro.start_recording(pattern)
        else:
            self.messageRecorded = True
            os.system(f"play -v {self.volume/100} audio/systemAudio/claque.ogg")
    
    def mode_1_stop_rec(self):
        ButtonRec.micro.stop_recording()
        self.audio.play_audio("audio/systemAudio/soundChanged.ogg", ButtonRec.volume)

    def mode_2_rec(self, pattern):
        audioGet = AudioGetter(pattern)
        audioFile = audioGet.get_audio()
        if "noMessageRecorded" in audioFile:
            self.messageRecorded = False
            ButtonRec.micro.start_recording(pattern)
        else:
            self.messageRecorded = True
            os.system(f"play -v {self.volume/100} audio/systemAudio/claque.ogg")
    
    def mode_2_stop_rec(self):
        ButtonRec.micro.stop_recording()
        self.audio.play_audio("audio/systemAudio/soundChanged.ogg", ButtonRec.volume)
        self.audio.play_audio("audio/systemAudio/start-mode-2.ogg", ButtonRec.volume)


    def mode_3_rec(self, pattern):
        self.audio.play_audio("audio/systemAudio/start-mode-3.ogg", ButtonRec.volume)
        ButtonRec.micro.start_recording(pattern)
    
    def mode_3_stop_rec(self):
        ButtonRec.micro.stop_recording()
        self.audio.play_audio("audio/systemAudio/start-mode-3.ogg", ButtonRec.volume)

    def action_button_on(self, mode, pattern):
        if mode == 1:
            self.mode_1_rec(pattern)
        elif mode == 2:
            self.mode_2_rec(pattern)
        elif mode == 3:
            self.mode_3_rec(pattern)

    def action_button_off(self, mode):
        if mode == 1:
            self.mode_1_stop_rec()
        elif mode == 2:
            self.mode_2_stop_rec()
        elif mode == 3:
            self.mode_3_stop_rec()
