from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Agents.ugve import UGVEAgent
from Classes.hospitalClass import Hospital as H
from Classes.emergencyVehicleClass import EmergencyVehicle as EV
from Classes.patientClass import Patient

import asyncio
import jsonpickle


class RescueMissionBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            performative = msg.get_metadata("performative")
            if performative == "request":
                self.agent.vehicle_info.setAvailable(False)
                ev_type = self.agent.vehicle_info.getType()
                if ev_type == "ambulancia":
                    await asyncio.sleep(3) #tempo para a ambulancia chegar ao paciente
                elif ev_type == "inem":
                    await asyncio.sleep(2) #tempo para o inem chegar ao paciente
                elif ev_type == "helicoptero":
                    await asyncio.sleep(1) #tempo para o helicoptero chegar ao paciente

                aid_request = jsonpickle.decode(msg.body)

                msg = Message(to=str(msg.sender))
                msg.body = jsonpickle.encode([self.agent.vehicle_info,aid_request.getSpecialty(),aid_request.getAgent(),self.agent.vehicle_info.getPositionX(),self.agent.vehicle_info.getPositionY()])
                msg.set_metadata("performative", "confirm")

                self.agent.vehicle_info.setPositionX(aid_request.getPositionX())
                self.agent.vehicle_info.setPositionY(aid_request.getPositionY())

                await self.send(msg)

            elif performative == "inform":

                aid_request = jsonpickle.decode(msg.body)

                if isinstance(aid_request[0], EV):

                    self.agent.vehicle_info.setAvailable(True)
                    self.agent.vehicle_info.setPositionX(aid_request[3])
                    self.agent.vehicle_info.setPositionY(aid_request[4])

                elif isinstance(aid_request[0], H):

                    ev_type = self.agent.vehicle_info.getType()
                    if ev_type == "ambulancia":
                        await asyncio.sleep(3)  # tempo para a ambulancia chegar ao hospital
                    elif ev_type == "inem":
                        await asyncio.sleep(2)  # tempo para o inem chegar ao hospital
                    elif ev_type == "helicoptero":
                        await asyncio.sleep(1)  # tempo para o helicoptero chegar ao hospital

                    position_x = aid_request[0].getLocation()[0]
                    position_y = aid_request[0].getLocation()[1]

                    msg = Message(to=str(msg.sender))
                    msg.body = jsonpickle.encode([self.agent.vehicle_info, position_x, position_y])
                    msg.set_metadata("performative", "inform")

                    self.agent.vehicle_info.setAvailable(True)
                    self.agent.vehicle_info.setPositionX(position_x)
                    self.agent.vehicle_info.setPositionY(position_y)

                    await self.send(msg)

            elif performative == "propose":
                info = jsonpickle.decode(msg.body)
                agent = info.getAgent()
                vehicle_type = info.getType()
                position_x = info.getPositionX()
                position_y = info.getPositionY()
                available = info.isAvailable()
                self.agent.vehicle_info = EV(agent,vehicle_type, position_x, position_y,available)

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not receive any message after 10 seconds")