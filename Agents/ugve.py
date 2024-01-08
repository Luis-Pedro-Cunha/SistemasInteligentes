from spade import agent
import random as rnd
from Behaviors.receiveRequestBehav import ReceiveRequestBehav
from Behaviors.heliportBehav import HeliportBehav
from Classes.emergencyVehicleClass import EmergencyVehicle
from Classes.hospitalClass import Hospital

class UGVEAgent(agent.Agent):

    emergency_vehicles = {}
    hospitals = {}
    specialties = ["cardio","pneumo","neuro","gastro","obstetricia"]

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        a = ReceiveRequestBehav()
        b = HeliportBehav(period=10)
        self.add_behaviour(a)
        self.add_behaviour(b)