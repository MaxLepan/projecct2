import json

class AudioGetter:

    def __init__(self, uid):
        self.uid = uid

    def get_audio(self):

        with open("./audio/audioStorage.json") as file:
            audioFile = json.load(file)
        return [item for item in audioFile["audioFiles"] if item.get(self.uid)][0][self.uid]


# audioGetter = AudioGetter(12)
# print(audioGetter.get_audio())