from spade import agent
from Behaviors.rescueMissionBehav import RescueMissionBehav
from Behaviors.subscribeEVehicleBehav import SubscribeEVehicleBehav
from Classes.emergencyVehicleClass import EmergencyVehicle
class EmergencyVehicleAgent(agent.Agent):

    vehicle_info = None

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = RescueMissionBehav()
        b = SubscribeEVehicleBehav()
        self.add_behaviour(a)
        self.add_behaviour(b)