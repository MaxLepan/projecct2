from .Micro import Micro

class ButtonRec:
    micro = Micro()

    def mode_1_audio(self):
        print("rec accompagner")

    def mode_1_rec(self, pattern):
        ButtonRec.micro.start_recording(pattern)
    
    def mode_1_stop_rec(self):
        ButtonRec.micro.stop_recording()

    def action(self, mode):
        if mode == 1:
            self.mode_1_audio()

    def action_button_on(self, mode, pattern):
        if mode == 1:
            self.mode_1_rec(pattern)

    def action_button_off(self, mode):
        if mode == 1:
            self.mode_1_stop_rec()