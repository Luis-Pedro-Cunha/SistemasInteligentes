class Patient:
    def __init__(self, agent_jid: str, status: str, specialty: str, position_x: int, position_y: int):
        self.agent_jid = agent_jid
        self.status = status
        self.specialty = specialty
        self.position_x = position_x
        self.position_y = position_y

    def getAgent(self):
        return self.agent_jid

    def getStatus(self):
        return self.status

    def setStatus(self, status: str):
        self.status = status

    def getSpecialty(self):
        return self.specialty

    def setSpecialty(self, specialty: str):
        self.specialty = specialty

    def getPositionX(self):
        return self.position_x

    def setPositionX(self, x: int):
        self.position_x = x

    def getPositionY(self):
        return self.position_y

    def setPositionY(self, y: int):
        self.position_y = y

    def toString(self):
        return "[Agent: " + self.agent_jid + ", Status: " + self.status + ", Specialty: " + self.specialty + ", X: " + str(self.position_x) + ", Y: " + str(self.position_y) + "]"