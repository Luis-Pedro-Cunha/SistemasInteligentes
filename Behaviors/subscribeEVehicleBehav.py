import random

from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.emergencyVehicleClass import EmergencyVehicle as EV
import jsonpickle

class SubscribeEVehicleBehav (OneShotBehaviour):
    async def run(self):
        vehicle_types = ["ambulancia","ambulancia","ambulancia","ambulancia","ambulancia","ambulancia","inem","inem","inem","helicoptero"]
        vehicle_type = random.choice(vehicle_types)
        position_x = random.randint(0,10000)
        position_y = random.randint(0,10000)
        self.agent.vehicle_info = EV(str(self.agent.jid),vehicle_type, position_x, position_y,True)
        print("Agent {}:".format(str(self.agent.jid)) + " Vehicle Agent initialized with {}".format(self.agent.vehicle_info.toString()))

        msg = Message(to=self.agent.get("receiveRequest_jid"))
        msg.body = jsonpickle.encode(self.agent.vehicle_info)
        msg.set_metadata("performative", "subscribe")

        print("Agent {}:".format(str(self.agent.jid)) + " Emergency Vehicle Agent subscribing to Manager Agent {}".format(str(self.agent.get("service_contact"))))
        await self.send(msg)