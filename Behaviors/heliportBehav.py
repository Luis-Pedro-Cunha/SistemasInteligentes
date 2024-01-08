from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from Classes.hospitalClass import Hospital
from Classes.emergencyVehicleClass import EmergencyVehicle
from Classes.patientClass import Patient

import asyncio
import jsonpickle


class HeliportBehav(PeriodicBehaviour):
    async def run(self):
        for hospital_key in self.agent.hospitals.keys():
            if self.agent.hospitals[hospital_key].getHeliport == "heliport_s":
                position_x = self.agent.hospitals[hospital_key].getLocation[0]
                position_y = self.agent.hospitals[hospital_key].getLocation[1]
                load = []
                for vehicle_key in self.agent.emergency_vehicles.keys():
                    vehicle = self.agent.emergency_vehicles[vehicle_key]
                    if vehicle.getType() == "helicoptero":
                        if position_x == vehicle.getPositionX and position_y == vehicle.getPositionY:
                            load.append(True)
                        else:
                            load.append(False)
                if True not in load:
                    self.agent.hospitals[hospital_key].setAvailable(True)

                    msg = Message(to=self.agent.hospitals[hospital_key].getAgent)
                    msg.body = jsonpickle.encode("Heliport is available")
                    msg.set_metadata("performative", "inform")


