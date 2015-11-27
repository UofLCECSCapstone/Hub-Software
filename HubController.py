#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import Database
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import dump
import xml.dom.minidom as MD

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
Motor1 = mh.getMotor(1)
Motor2 = mh.getMotor(2)
Motor3 = mh.getMotor(3)
Motor4 = mh.getMotor(4)

###################
##### Methods #####
###################
def UpdateDeviceStatus():
    """
    Reads the current state of each device connected to the hub, and
    updates the program's internal representation of that state.
    """
    UpdateDoorStatus()
    UpdateThermostatStatus()
    UpdateLightStatus()

def UpdateDoorStatus():
    """
    Checks each door connected to the hub, to see if it is opened or closed.
    """
    # print("Checking door 1 status...")
    # print("Checking door 2 status...")
    # print("...")
    # print("Checking door n status...")

def UpdateThermostatStatus():
    """
    Checks the current temperature that the thermostat is set at.
    """
    # print("Checking thermostat temperature...")

def UpdateLightStatus():
    """
    Checks each lightbulb connected to the hub, to see if it is turned on or off.
    """
    # print("Checking lightbulb 1 status...")
    # print("Checking lightbulb 2 status...")
    # print("...")
    # print("Checking lightbulb n status...")

    
class HubController:
    """
    Class that provides the interface between connected hardware devices
    and the Android phone controlling the devices.
    """

    #################################
    ##### Command abbreviations #####
    #################################
    CMD_GET_DOOR_STATUS = "GetDoorStatus"
    CMD_GET_LIGHT_STATUS = "GetLightStatus"
    CMD_GET_TEMPERATURE_STATUS = "GetTemperatureStatus"
    CMD_OPEN_DOOR = "OpenDoor"

    def __init__(self):
        print("Initializing!")

        
        # set the speed to start, from 0 (off) to 255 (max speed)
        # Initialize all motors
        for motor in (Motor1, Motor2, Motor3, Motor4):
            motor.setSpeed(150)
            motor.run(Adafruit_MotorHAT.FORWARD);
            # turn on motor
            motor.run(Adafruit_MotorHAT.RELEASE);
            print("Motor " + str(motor.motornum) + " initialized.")

    def PerformCommand(self, commandAbbreviation, optArg):
        """
        Performs the command represented by the provided command abbreviation.
        :param commandAbbreviation: An abbreviation representing the command to execute.
        :return Returns a string, with the result of performing the command.
        """
        self.log("Performing the command: " + commandAbbreviation)

        # TODO What if processing a command fails? Should it still be removed from the queue, which is what happens when .get() is called?
        if commandAbbreviation == self.CMD_GET_DOOR_STATUS:
            # Here's the response format for this command:
            # <Doors>
            #     <Door ID="1" Status="Open"/>
            #     <Door ID="2" Status="Closed"/>
            #     <Door ID="3" Status="Closed"/>
            #     <Door ID="4" Status="Open"/>
            # </Doors>
            xmlDoorsRoot = ET.Element('Doors')
            
            conn = Database.get_connection()
            cursor = conn.cursor()

            # TODO Move this logic into a separate Door class.
            # TODO What if in the database there's a value other than 1 or 0? How should we parse that?
            for door in cursor.execute('SELECT ID, blnOpen FROM Door'):
                ET.SubElement(xmlDoorsRoot,
                              'Door',
                              # TODO Convert these hard-coded indices (door[0], door[1]) into constants - door[IX_ID], door[IX_Open].
                              ID=str(door[0]),
                              Status=("Open" if door[1] == 1 else "Closed"))
            conn.close() 

            return (ET.tostring(xmlDoorsRoot, encoding="utf-8", method="xml")).decode('utf8')
            # ET.tostring(xmlDoorsRoot) # xmlDoorsRoot.tostring()
        elif commandAbbreviation == self.CMD_GET_LIGHT_STATUS:
            return "Getting light status..."
        elif commandAbbreviation == self.CMD_GET_TEMPERATURE_STATUS:
            return "Getting temperature status..."
        elif commandAbbreviation == self.CMD_OPEN_DOOR:
            # TODO Return different text depending on success/failure.
            CurrentMotor = None
            MotorNumber = str(optArg)
            if optArg == "1":
                CurrentMotor = Motor1
            elif optArg == "2":
                CurrentMotor = Motor2
            elif optArg == "3":
                CurrentMotor = Motor3
            elif optArg == "4":
                CurrentMotor = Motor4
            else:
                print("TODO How should we handle this?")
            print(MotorNumber)
            print(CurrentMotor)
                
            print("Forward!")
            CurrentMotor.run(Adafruit_MotorHAT.FORWARD)

            print("\tSpeed up...")
            for i in range(255):
                CurrentMotor.setSpeed(i)
                time.sleep(0.01)

            print("\tSlow down...")
            for i in reversed(range(255)):
                CurrentMotor.setSpeed(i)
                time.sleep(0.01)

            print("Backward! ")
            CurrentMotor.run(Adafruit_MotorHAT.BACKWARD)

            print("\tSpeed up...")
            for i in range(255):
                CurrentMotor.setSpeed(i)
                time.sleep(0.01)

            print("\tSlow down...")
            for i in reversed(range(255)):
                CurrentMotor.setSpeed(i)
                time.sleep(0.01)

            print("Release")
            CurrentMotor.run(Adafruit_MotorHAT.RELEASE)
            time.sleep(1.0)

            return "Door " + MotorNumber + " opened or closed."
        elif commandAbbreviation == "":
            log("TODO Testing")
            # No command found.
        else:
            return "TODO Handle this case somehow."

    # TODO I need to keep a couple of log files - HubLog, for commands executed on the hub,
    #      and HTTPServerLog, for commands sent to the HTTP server. Or log them both to a database.

    def log(self, message):
        print("HubControler::" + message)

#######################
##### Main method #####
#######################
def main():
    try:
        controller = HubController()
        while True:
            UpdateDeviceStatus()
            controller.CheckForCommands()
    except:
        print("TODO Handle errors here appropriately. Exit the program?")

if __name__ == "__main__":
    main()
