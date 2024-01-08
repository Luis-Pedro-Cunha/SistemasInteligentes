class EmergencyVehicle:
    def __init__(self, agent_jid: str, type: str, position_x: int, position_y: int, available: bool):
        self.agent_jid = agent_jid
        self.type = type
        self.position_x = position_x
        self.position_y = position_y
        self.available = available

    def getAgent(self):
        return self.agent_jid

    def getType(self):
        return self.type

    def setType(self, type: str):
        self.type = type

    def getPositionX(self):
        return self.position_x

    def setPositionX(self, x: int):
        self.position_x = x

    def getPositionY(self):
        return self.position_y

    def setPositionY(self, y: int):
        self.position_y = y
    def isAvailable(self):
        return self.available
    def setAvailable(self, available: bool):
        self.available = available
    def toString(self):
        return "[Type: " + self.type + ", X: " + str(self.position_x) + ", Y: " + str(self.position_y) + ", Available: " + str(self.available) + "]"