import uuid
import json


class AudioStoring:

    def __init__(self, file, uid):
        self.file = file
        self.uid = uid
        self.list_obj = []

    def store(self):

        audio = {self.uid: self.file}

        with open("./audio/audioStorage.json") as file:

            self.list_obj = json.load(file)
        
        if len(self.list_obj["audioFiles"]) > 0:
            for item in self.list_obj["audioFiles"]:
                print(item)
                if item.get(self.uid):
                    item[self.uid] = self.file
                    break
                else:
                    self.list_obj["audioFiles"].append(audio)
        else:
            self.list_obj["audioFiles"].append(audio)
            
        with open("./audio/audioStorage.json", "w") as file:
            json.dump(self.list_obj, file, indent=4, separators=(',', ': '))


# Uncomment to run tests
# audio_storing = AudioStoring("./audio/audioFiles/audio.ogg", 13)
# audio_storing.store()
