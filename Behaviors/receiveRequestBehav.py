import jsonpickle
from spade.behaviour import CyclicBehaviour
import math
from spade.message import Message
from Classes.hospitalClass import Hospital as H
from Classes.emergencyVehicleClass import EmergencyVehicle as EV
from Classes.patientClass import Patient as P

class ReceiveRequestBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            performative = msg.get_metadata("performative")
            if performative == "subscribe":
                info = jsonpickle.decode(msg.body)
                if isinstance(info, H):
                    hospital_num = len(self.agent.hospitals.keys())
                    if hospital_num == 0:
                        info.setHeliport("heliport_s")
                        info.setAvailable(True)
                        info.setSpecialties({"cardio":25, "pneumo":25, "neuro":25, "gastro":25, "obstetricia":25})
                        self.agent.hospitals[("hospital" + str(hospital_num + 1))] = info
                        msg = Message(to=info.getAgent())
                        msg.body = jsonpickle.encode(info)
                        msg.set_metadata("performative", "propose")
                        await self.send(msg)

                    else:
                        self.agent.hospitals[("hospital" + str(hospital_num + 1))] = info
                elif isinstance(info, EV):
                    vehicle_num = len(self.agent.emergency_vehicles.keys())
                    if vehicle_num == 0:
                        info.setType("ambulancia")
                        self.agent.emergency_vehicles[("veículo" + str(vehicle_num + 1))] = info
                        msg = Message(to=info.getAgent())
                        msg.body = jsonpickle.encode(info)
                        msg.set_metadata("performative", "propose")
                        await self.send(msg)
                    elif vehicle_num == 1:
                        info.setType("inem")
                        self.agent.emergency_vehicles[("veículo" + str(vehicle_num + 1))] = info
                        msg = Message(to=info.getAgent())
                        msg.body = jsonpickle.encode(info)
                        msg.set_metadata("performative", "propose")
                        await self.send(msg)
                    elif vehicle_num == 2:
                        info.setType("helicoptero")
                        self.agent.emergency_vehicles[("veículo" + str(vehicle_num + 1))] = info
                        msg = Message(to=info.getAgent())
                        msg.body = jsonpickle.encode(info)
                        msg.set_metadata("performative", "propose")
                        await self.send(msg)
                    else:
                        self.agent.emergency_vehicles[("veículo" + str(vehicle_num+1))] = info
                else:
                    print("Agent {}:".format(str(self.agent.jid)) + " Message type not understood!")

            elif performative == "request":
                print("Agent {}:".format(str(self.agent.jid)) + " Client Agent {} requested aid!".format(str(msg.sender)))
                aid_request = jsonpickle.decode(msg.body)
                position_x = aid_request.getPositionX()
                position_y = aid_request.getPositionY()
                status = aid_request.getStatus()

                if status == "ligeiro":
                    key_name = ""
                    min_dist = 10000

                    for key in self.agent.emergency_vehicles.keys():
                        e_vehicle = self.agent.emergency_vehicles[key]
                        if e_vehicle.getType() == "ambulancia":
                            if self.agent.emergency_vehicles[key].isAvailable():
                                distance = math.sqrt(
                                    math.pow(e_vehicle.getPositionX() - position_x, 2) +
                                    math.pow(e_vehicle.getPositionY() - position_y, 2)
                                )
                                if (min_dist > distance):
                                    key_name = key
                                    min_dist = distance
                    if key_name != "":
                        print("Agent {}:".format(
                            str(self.agent.jid)) + " Rescue vehicle {} selected for Rescue Request!".format(
                            key_name))

                        msg = Message(to=self.agent.emergency_vehicles[key_name].getAgent())
                        msg.body = jsonpickle.encode(aid_request)
                        msg.set_metadata("performative", "request")
                        await self.send(msg)

                        self.agent.emergency_vehicles[key_name].setAvailable(False)
                        self.agent.emergency_vehicles[key_name].setPositionX(position_x)
                        self.agent.emergency_vehicles[key_name].setPositionY(position_y)

                    else:
                        print("Agent {}:".format(str(self.agent.jid)) + " No Vehicles available!")
                        msg = msg.make_reply()
                        msg.set_metadata("performative", "refuse")
                        await self.send(msg)


                elif status == "grave":
                    key_name = ""
                    min_dist = 10000

                    for key in self.agent.emergency_vehicles.keys():
                        e_vehicle = self.agent.emergency_vehicles[key]
                        if e_vehicle.getType() == "inem":
                            if self.agent.emergency_vehicles[key].isAvailable():
                                distance = math.sqrt(
                                    math.pow(e_vehicle.getPositionX() - position_x, 2) +
                                    math.pow(e_vehicle.getPositionY() - position_y, 2)
                                )
                                if (min_dist > distance):
                                    key_name = key
                                    min_dist = distance
                    if key_name != "":
                        print("Agent {}:".format(
                            str(self.agent.jid)) + " Rescue vehicle {} selected for Rescue Request!".format(
                            key_name))

                        msg = Message(to=self.agent.emergency_vehicles[key_name].getAgent())
                        msg.body = jsonpickle.encode(aid_request)
                        msg.set_metadata("performative", "request")
                        await self.send(msg)

                        self.agent.emergency_vehicles[key_name].setAvailable(False)
                        self.agent.emergency_vehicles[key_name].setPositionX(position_x)
                        self.agent.emergency_vehicles[key_name].setPositionY(position_y)

                    else:
                        print("Agent {}:".format(str(self.agent.jid)) + " No INEM available! Finding an Ambulance!")
                        key_name = ""
                        min_dist = 10000

                        for key in self.agent.emergency_vehicles.keys():
                            e_vehicle = self.agent.emergency_vehicles[key]
                            if e_vehicle.getType() == "ambulancia":
                                if self.agent.emergency_vehicles[key].isAvailable():
                                    distance = math.sqrt(
                                        math.pow(e_vehicle.getPositionX() - position_x, 2) +
                                        math.pow(e_vehicle.getPositionY() - position_y, 2)
                                    )
                                    if (min_dist > distance):
                                        key_name = key
                                        min_dist = distance
                        if key_name != "":
                            print("Agent {}:".format(
                                str(self.agent.jid)) + " Rescue vehicle {} selected for Rescue Request!".format(
                                key_name))

                            msg = Message(to=self.agent.emergency_vehicles[key_name].getAgent())
                            msg.body = jsonpickle.encode(aid_request)
                            msg.set_metadata("performative", "request")
                            await self.send(msg)

                            self.agent.emergency_vehicles[key_name].setAvailable(False)
                            self.agent.emergency_vehicles[key_name].setPositionX(position_x)
                            self.agent.emergency_vehicles[key_name].setPositionY(position_y)


                        else:
                            print("Agent {}:".format(str(self.agent.jid)) + " No Vehicles available!")
                            msg = msg.make_reply()
                            msg.set_metadata("performative", "refuse")
                            await self.send(msg)

                elif status == "muito grave":
                    point = 0
                    for key in self.agent.hospitals.keys():
                        hospital_key = key
                        if self.agent.hospitals[hospital_key].isAvailable():
                            key_name = ""
                            min_dist = 10000

                            for key in self.agent.emergency_vehicles.keys():
                                e_vehicle = self.agent.emergency_vehicles[key]
                                if e_vehicle.getType() == "helicoptero":
                                    if self.agent.emergency_vehicles[key].isAvailable():
                                        distance = math.sqrt(
                                            math.pow(e_vehicle.getPositionX() - position_x, 2) +
                                            math.pow(e_vehicle.getPositionY() - position_y, 2)
                                        )
                                        if (min_dist > distance):
                                            key_name = key
                                            min_dist = distance
                            if key_name != "":
                                print("Agent {}:".format(
                                    str(self.agent.jid)) + " Rescue vehicle {} selected for Rescue Request!".format(
                                    key_name))

                                msg = Message(to=self.agent.emergency_vehicles[key_name].getAgent())
                                msg.body = jsonpickle.encode(aid_request)
                                msg.set_metadata("performative", "request")
                                await self.send(msg)

                                self.agent.emergency_vehicles[key_name].setAvailable(False)
                                self.agent.emergency_vehicles[key_name].setPositionX(position_x)
                                self.agent.emergency_vehicles[key_name].setPositionY(position_y)

                            else:
                                print("Agent {}:".format(
                                    str(self.agent.jid)) + " No Helicopters available! Finding an INEM!")
                                point = 1
                        else:
                            print("Agent {}:".format(
                                str(self.agent.jid)) + " No Heliports available! Finding an INEM!")
                            point = 1
                            break
                    if point == 1:
                        key_name = ""
                        min_dist = 10000

                        for key in self.agent.emergency_vehicles.keys():
                            e_vehicle = self.agent.emergency_vehicles[key]
                            if e_vehicle.getType() == "inem":
                                if self.agent.emergency_vehicles[key].isAvailable():
                                    distance = math.sqrt(
                                        math.pow(e_vehicle.getPositionX() - position_x, 2) +
                                        math.pow(e_vehicle.getPositionY() - position_y, 2)
                                    )
                                    if (min_dist > distance):
                                        key_name = key
                                        min_dist = distance
                        if key_name != "":
                            print("Agent {}:".format(
                                str(self.agent.jid)) + " Rescue vehicle {} selected for Rescue Request!".format(
                                key_name))

                            msg = Message(to=self.agent.emergency_vehicles[key_name].getAgent())
                            msg.body = jsonpickle.encode(aid_request)
                            msg.set_metadata("performative", "request")
                            await self.send(msg)

                            self.agent.emergency_vehicles[key_name].setAvailable(False)
                            self.agent.emergency_vehicles[key_name].setPositionX(position_x)
                            self.agent.emergency_vehicles[key_name].setPositionY(position_y)


                        else:
                            print("Agent {}:".format(str(self.agent.jid)) + " No INEM available! Finding an Ambulance!")
                            key_name = ""
                            min_dist = 10000

                            for key in self.agent.emergency_vehicles.keys():
                                e_vehicle = self.agent.emergency_vehicles[key]
                                if e_vehicle.getType() == "ambulancia":
                                    if self.agent.emergency_vehicles[key].isAvailable():
                                        distance = math.sqrt(
                                            math.pow(e_vehicle.getPositionX() - position_x, 2) +
                                            math.pow(e_vehicle.getPositionY() - position_y, 2)
                                        )
                                        if (min_dist > distance):
                                            key_name = key
                                            min_dist = distance
                            if key_name != "":
                                print("Agent {}:".format(
                                    str(self.agent.jid)) + " Rescue vehicle {} selected for Rescue Request!".format(
                                    key_name))

                                msg = Message(to=self.agent.emergency_vehicles[key_name].getAgent())
                                msg.body = jsonpickle.encode(aid_request)
                                msg.set_metadata("performative", "request")
                                await self.send(msg)

                                self.agent.emergency_vehicles[key_name].setAvailable(False)
                                self.agent.emergency_vehicles[key_name].setPositionX(position_x)
                                self.agent.emergency_vehicles[key_name].setPositionY(position_y)

                            else:
                                print("Agent {}:".format(str(self.agent.jid)) + " No Vehicles available!")
                                msg = msg.make_reply()
                                msg.set_metadata("performative", "refuse")
                                await self.send(msg)


            elif performative == "confirm":
                aid_request = jsonpickle.decode(msg.body)
                if isinstance(aid_request[0], EV):
                    print("Agent {}:".format(str(self.agent.jid)) + " Emergency Vehicle Agent {} confirmed rescue!".format(
                        str(msg.sender)))
                    vehicle_type = aid_request[0].getType()
                    position_x = aid_request[0].getPositionX()
                    position_y = aid_request[0].getPositionY()
                    specialty = aid_request[1]
                    vehicle_agent = aid_request[0].getAgent()
                    patient_agent = aid_request[2]
                    key_name = ""
                    min_dist = 10000

                    for key in self.agent.hospitals.keys():
                        hospital_key = key
                        if specialty in self.agent.hospitals[hospital_key].getSpecialties().keys():
                            vacancies = self.agent.hospitals[key].getSpecialties()[specialty]
                            if vacancies > 0:
                                distance = math.sqrt(
                                    math.pow(self.agent.hospitals[hospital_key].getLocation()[0] - position_x, 2) +
                                    math.pow(self.agent.hospitals[hospital_key].getLocation()[1] - position_y, 2)
                                )
                                if (min_dist > distance):
                                    key_name = key
                                    min_dist = distance

                    if key_name != "":
                        print("Agent {}:".format(str(self.agent.jid)) + " Hospital {} selected for Aid Request!".format(key_name))
                        msg = Message(to=self.agent.hospitals[key_name].getAgent())
                        msg.body = jsonpickle.encode(aid_request)
                        msg.set_metadata("performative", "request")
                        await self.send(msg)

                        if vehicle_type == "helicoptero":
                            self.agent.hospitals[key_name].setAvailable(False)

                        vacancies = self.agent.hospitals[key_name].getSpecialties()[specialty]
                        self.agent.hospitals[key_name].editSpecialties(specialty,(vacancies - 1))

                    else:
                        print("Agent {}:".format(str(self.agent.jid)) + " No Hospitals available!")
                        msg1 = Message(to=patient_agent)
                        msg1.set_metadata("performative", "refuse")

                        msg2 = Message(to=vehicle_agent)
                        msg2.body = jsonpickle.encode(aid_request)
                        msg2.set_metadata("performative", "inform")

                        await self.send(msg1)
                        await self.send(msg2)

                elif isinstance(aid_request[0], H):
                    print("Agent {}:".format(str(self.agent.jid)) + " Hospital Agent {} confirmed arrival!".format(
                        str(msg.sender)))
                    aid_request = jsonpickle.decode(msg.body)
                    patient_agent = aid_request[2]
                    vehicle_agent = aid_request[1]

                    msg1 = Message(to=vehicle_agent)
                    msg1.body = jsonpickle.encode(aid_request)
                    msg1.set_metadata("performative", "inform")

                    msg2 = Message(to=str(msg.sender))
                    msg2.body = jsonpickle.encode(aid_request)
                    msg2.set_metadata("performative", "inform")

                    msg3 = Message(to=patient_agent)
                    msg3.set_metadata("performative", "confirm")

                    await self.send(msg1)
                    await self.send(msg2)
                    await self.send(msg3)

            elif performative == "inform":
                info = jsonpickle.decode(msg.body)
                if isinstance(info[0], H):
                    specialty = info[1]
                    for key, value in self.agent.hospitals.items():
                        if value.getAgent() == info[0].getAgent():
                            vacancies = self.agent.hospitals[key].getSpecialties()[specialty]
                            self.agent.hospitals[key].editSpecialties(specialty, (vacancies + 1))

                elif isinstance(info[0], EV):
                    position_x = info[1]
                    position_y = info[2]
                    for key, value in self.agent.emergency_vehicles.items():
                        if value.getAgent() == info[0].getAgent():
                            self.agent.emergency_vehicles[key].setAvailable(True)
                            self.agent.emergency_vehicles[key].setPositionX(position_x)
                            self.agent.emergency_vehicles[key].setPositionY(position_y)

                else:
                    print("Agent {}:".format(str(self.agent.jid)) + " Message type not understood!")

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not receive any message after 10 seconds")
