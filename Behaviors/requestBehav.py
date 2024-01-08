import random

from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Classes.patientClass import Patient as P

import jsonpickle

class RequestBehav (OneShotBehaviour):
    async def run(self):

        specialties = ["cardio","pneumo","neuro","gastro","obstetricia"]
        patient_state = ["ligeiro","grave","muito grave"]
        specialty = random.choice(specialties)
        status = random.choice(patient_state)
        position_x = random.randint(0, 10000)
        position_y = random.randint(0, 10000)

        patient = P(str(self.agent.jid),status,specialty,position_x,position_y)
        msg = Message(to=self.agent.get("receiveRequest_jid"))
        msg.set_metadata("performative", "request")
        msg.body = jsonpickle.encode(patient)
        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent requesting emergency service to Manager Agent {}".format(str(self.agent.get("receiveRequest_jid"))))
        await self.send(msg)
