import json

class AudioGetter:

    def __init__(self, uid):
        self.uid = str(uid)

    def get_audio(self):
        with open("./audio/audioStorage.json") as file:
            audioFile = json.load(file)
        for item in audioFile["audioFiles"]:
            if item.get(self.uid):
                return item[self.uid]
        #return [item for item in audioFile["audioFiles"] if item.get(self.uid)]
        return "audio/audioFiles/test.ogg"


#audioGetter = AudioGetter(0)
#print(audioGetter.get_audio())