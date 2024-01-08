import time
from spade import quit_spade

from Agents.emergencyVehicle import EmergencyVehicleAgent
from Agents.hospital import HospitalAgent
from Agents.patient import PatientAgent
from Agents.ugve import UGVEAgent

XMPP_SERVER = 'localhost'
PASSWORD = 'NOPASSWORD'

MAX_PATIENTS = 100
MAX_VEHICLES = 30
MAX_HOSPITALS = 10

if __name__ == '__main__':

    patient_agents_list = []

    ugve_jid = 'ugve@' + XMPP_SERVER
    ugve_agent = UGVEAgent(ugve_jid, PASSWORD)

    res_ugve = ugve_agent.start(auto_register=True)
    res_ugve.result()

    time.sleep(1)

    for i in range(1, MAX_HOSPITALS + 1):
        hospital_jid = 'hospital{}@'.format(str(i)) + XMPP_SERVER
        hospital_agent = HospitalAgent(hospital_jid, PASSWORD)

        hospital_agent.set('receiveRequest_jid', ugve_jid)

        res_hospital = hospital_agent.start(auto_register=True)
        res_hospital.result()

    time.sleep(1)

    for j in range(1, MAX_VEHICLES + 1):
        emergency_vehicle_jid = 'emergency_vehicle{}@'.format(str(j)) + XMPP_SERVER
        emergency_vehicle_agent = EmergencyVehicleAgent(emergency_vehicle_jid, PASSWORD)

        emergency_vehicle_agent.set('receiveRequest_jid', ugve_jid)

        res_emergency_vehicle = emergency_vehicle_agent.start(auto_register=True)
        res_emergency_vehicle.result()

    time.sleep(1)

    for k in range(1, MAX_PATIENTS + 1):

        if k % 5 == 0:
            time.sleep(1)

        patient_jid = 'patient{}@'.format(str(k)) + XMPP_SERVER
        patient_agent = PatientAgent(patient_jid, PASSWORD)

        patient_agent.set("receiveRequest_jid", ugve_jid)

        res_patient = patient_agent.start(auto_register=True)
        res_patient.result()
        patient_agents_list.append(patient_agent)

    while ugve_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            hospital_agent.stop()
            emergency_vehicle_agent.stop()
            for patient_agent in patient_agents_list:
                patient_agent.stop()
            break
    print('Agents finished')

    quit_spade()
