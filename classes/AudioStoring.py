import uuid
import json


class AudioStoring:

    def __init__(self, file, uid):
        self.file = file
        self.uid = str(uid)
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
                    break
        else:
            self.list_obj["audioFiles"].append(audio)
            
            
        with open("./audio/audioStorage.json", "w") as file:
            json.dump(self.list_obj, file, indent=4, separators=(',', ': '))

    
    def deleteAudio(self):
        
        with open("./audio/audioStorage.json") as file:

            self.list_obj = json.load(file)
        print(self.list_obj["audioFiles"])
        if len(self.list_obj["audioFiles"]) > 0:
            for item in self.list_obj["audioFiles"]:
                print(item)
                if item.get(self.uid):
                    print("yahoo")
                    #self.list_obj["audioFiles"].pop(item)
                    index = self.list_obj["audioFiles"].index(item)
                    del self.list_obj["audioFiles"][index]
                    print(self.list_obj["audioFiles"], "32")
                    break
          
        with open("./audio/audioStorage.json", "w") as file:
            json.dump(self.list_obj, file, indent=4, separators=(',', ': '))
            
        print("Deleted")
        
        
# Uncomment to run tests
# audio_storing = AudioStoring("./audio/audioFiles/audio.ogg", 13)
# audio_storing.store()
# audio_storing.delete()