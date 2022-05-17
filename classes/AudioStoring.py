import json
import os


class AudioStoring:

    def __init__(self, file, uid):
        self.file = file
        self.uid = str(uid)
        self.list_obj = []
        volumeFile = open("./database/sound-volume.txt", "r")
        self.volume = int(volumeFile.readline())

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
                    break
        else:
            self.list_obj["audioFiles"].append(audio)

        with open("./audio/audioStorage.json", "w") as file:
            json.dump(self.list_obj, file, indent=4, separators=(',', ': '))

        os.system("play audio/systemAudio/messageRegistered.ogg")

    def deleteAudio(self):
        
        with open("./audio/audioStorage.json") as file:

            self.list_obj = json.load(file)
        print(self.list_obj["audioFiles"])
        if len(self.list_obj["audioFiles"]) > 0:
            for item in self.list_obj["audioFiles"]:
                if item.get(self.uid):
                    index = self.list_obj["audioFiles"].index(item)
                    del self.list_obj["audioFiles"][index]
                    os.system(f"play -v {self.volume/100} audio/systemAudio/messageDeleted.ogg")
                    break
                else:
                    print("no mess del")
                    os.system(f"play -v {self.volume/100} audio/systemAudio/claque.ogg")
          
        with open("./audio/audioStorage.json", "w") as file:
            json.dump(self.list_obj, file, indent=4, separators=(',', ': '))


        print("Deleted")
        
        
# Uncomment to run tests
# audio_storing = AudioStoring("./audio/audioFiles/audio.ogg", 13)
# audio_storing.store()
# audio_storing.delete()