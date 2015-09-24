# TODO It would be useful to log, probably in a file, each command that is executed/received/etc. Same goes for the HTTP server.
# TODO Create classes that represent each type of peripheral - Lightbulb, Thermostat, Door -
#      and populate objects of those classes in the below methods, to keep things logically separated out.
#      Procedural spaghetti is bad.
# TODO This should probably be converted into a class.

import queue

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

    CommandQueue = queue.Queue()

    def CheckForCommands(self):
        """
        Checks to see if the user has requested that a command be performed.
        If so, the command is performed.
        """
        # print("Checking for commands from the user...")
        # print("TODO Fill this in with actual checks.")
        commandAbbreviation = self.CommandQueue.get()

        # TODO What if processing a command fails? Should it still be removed from the queue, which is what happens when .get() is called?
        if commandAbbreviation == self.CMD_GET_DOOR_STATUS:
            return "Door status is ok."
        elif commandAbbreviation == self.CMD_GET_LIGHT_STATUS:
            return "Getting light status..."
        elif commandAbbreviation == self.CMD_GET_TEMPERATURE_STATUS:
            return "Getting temperature status..."
        elif commandAbbreviation == "":
            log("TODO Testing")
            # No command found.
        else:
            return "TODO Handle this case somehow."

    def PushCommand(self, commandAbbreviation):
        """
        Pushes a command to the hub controller's queue of commands to be processed.
        :param commandAbbreviation: An abbreviation representing the command to execute.
        """
        self.CommandQueue.put(commandAbbreviation)
        self.log("Received command: " + commandAbbreviation)

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
