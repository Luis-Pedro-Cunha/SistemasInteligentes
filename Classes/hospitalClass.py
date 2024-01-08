class Hospital:
    def __init__(self, agent_jid: str, heliport: str, specialties: dict, location: list, available: bool):
        self.agent_jid = agent_jid
        self.heliport = heliport
        self.specialties = specialties
        self.location = location
        self.available = available

    def getAgent(self):
        return self.agent_jid

    def getLocation(self):
        return self.location

    def setLocation(self, x: int, y: int):
        self.location = [x,y]

    def getHeliport(self):
        return self.heliport

    def setHeliport(self, h: str):
        self.heliport = h

    def getSpecialties(self):
        return self.specialties

    def setSpecialties(self, s_dict: dict):
        self.specialties = s_dict

    def editSpecialties(self, key: str, vacancies: int):
        self.specialties[key] = vacancies

    def isAvailable(self):
        return self.available
    def setAvailable(self, available: bool):
        self.available = available
    def toString(self):
        return "[Heliport?: " + self.heliport + ", Specialties: " + str(self.specialties) + ", Location: " + str(self.location) + ", Available: " + str(self.available) + "]"