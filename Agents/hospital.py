from spade import agent
from Behaviors.hospitalBehav import HospitalBehav
from Behaviors.subscribeHospitalBehav import SubscribeHospitalBehav
from Classes.hospitalClass import Hospital
class HospitalAgent(agent.Agent):

    hospital_info = None

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = HospitalBehav()
        b = SubscribeHospitalBehav()
        self.add_behaviour(a)
        self.add_behaviour(b)