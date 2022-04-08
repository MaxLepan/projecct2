
class ProtocolReader:
    
    def __init__(self, data):
        
        self.data = data

    def decodeProtocol(self):
        
        spliced_data = self.data.split(":")
        self.sensor = spliced_data[0]
        self.value = spliced_data[1]
        