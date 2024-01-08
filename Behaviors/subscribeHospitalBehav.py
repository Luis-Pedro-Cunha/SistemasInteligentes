import random

from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.hospitalClass import Hospital as H
import jsonpickle

class SubscribeHospitalBehav (OneShotBehaviour):
    async def run(self):
        has_heliport = ["heliport_s","heliport_n"]
        possible_specialties = ["cardio", "pneumo", "neuro", "gastro", "obstetricia"]
        specialty_num = random.randint(1,5)
        specialties = {}
        location = [random.randint(0,10000),random.randint(0,10000)]
        heliport = random.choice(has_heliport)
        available = False
        if heliport == "heliport_s":
            available = True
        i = 0
        while i < specialty_num:
            specialty = random.choice(possible_specialties)
            possible_specialties.remove(specialty)
            specialties[specialty] = random.randrange(5,26,5)
            i += 1

        self.agent.hospital_info = H(str(self.agent.jid),heliport,specialties,location,available)
        print("Agent {}:".format(str(self.agent.jid)) + " Hospital Agent initialized with {}".format(self.agent.hospital_info.toString()))

        msg = Message(to=self.agent.get("receiveRequest_jid"))
        msg.body = jsonpickle.encode(self.agent.hospital_info)
        msg.set_metadata("performative", "subscribe")

        print("Agent {}:".format(str(self.agent.jid)) + " Hospital Agent subscribing to Manager Agent {}".format(str(self.agent.get("receiveRequest_jid"))))
        await self.send(msg)