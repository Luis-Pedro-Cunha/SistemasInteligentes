from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Classes.hospitalClass import Hospital as H
from Classes.emergencyVehicleClass import EmergencyVehicle
from Classes.patientClass import Patient

import asyncio
import jsonpickle


class HospitalBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            performative = msg.get_metadata("performative")

            if performative == "request":

                aid_request = jsonpickle.decode(msg.body)
                vehicle_type = aid_request[0].getType()
                specialty = aid_request[1]
                vehicle_agent = aid_request[0].getAgent()
                patient_agent = aid_request[2]

                if vehicle_type == "helicoptero":
                    self.agent.hospital_info.setAvailable(False)

                vacancies = self.agent.hospital_info.getSpecialties()[specialty]
                self.agent.hospital_info.editSpecialties(specialty, (vacancies - 1))

                msg = Message(to=str(msg.sender))
                msg.body = jsonpickle.encode([self.agent.hospital_info, vehicle_agent, patient_agent, specialty])
                msg.set_metadata("performative", "confirm")

                await self.send(msg)

            elif performative == "inform":

                message = jsonpickle.decode(msg.body)

                if isinstance(message, str):
                    self.agent.hospital_info.setAvailable(True)

                else:

                    await asyncio.sleep(1)  # tempo para a recuperação do paciente

                    specialty = message[3]

                    msg = Message(to=str(msg.sender))
                    msg.body = jsonpickle.encode([self.agent.hospital_info,specialty])
                    msg.set_metadata("performative", "inform")

                    vacancies = self.agent.hospital_info.getSpecialties()[specialty]
                    self.agent.hospital_info.editSpecialties(specialty, (vacancies + 1))

                    await self.send(msg)

            elif performative == "propose":
                info = jsonpickle.decode(msg.body)
                agent = info.getAgent()
                heliport = info.getHeliport()
                specialties = info.getSpecialties()
                location = info.getLocation()
                available = info.isAvailable()
                self.agent.hospital_info = H(agent, heliport, specialties, location, available)

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")


        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not receive any message after 10 seconds")