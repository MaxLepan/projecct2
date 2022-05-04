
class ProtocolBuilder:
    
    def __init__(self, sensor, value):
        self.sensor = sensor
        self.value = value
    
    def buildProtocol(self):
        return self.sensor + ":" + str(self.value)
    