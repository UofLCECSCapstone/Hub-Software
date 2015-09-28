#! python

# TODO Create classes that represent each type of peripheral - Lightbulb, Thermostat, Door -
#      and populate objects of those classes in the below methods, to keep things logically separated out.
#      Procedural spaghetti is bad.
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
    print("Checking door 1 status...")
    print("Checking door 2 status...")
    print("...")
    print("Checking door n status...")

def UpdateThermostatStatus():
    """
    Checks the current temperature that the thermostat is set at.
    """
    print("Checking thermostat temperature...")

def UpdateLightStatus():
    """
    Checks each lightbulb connected to the hub, to see if it is turned on or off.
    """
    print("Checking lightbulb 1 status...")
    print("Checking lightbulb 2 status...")
    print("...")
    print("Checking lightbulb n status...")

def CheckForCommands():
    """
    Checks to see if the user has requested that a command be performed.
    If so, the command is performed.
    """
    print("Checking for commands from the user...")
    print("TODO Fill this in with actual checks.")

#######################
##### Main method #####
#######################
def main():
    try:
        while True:
            UpdateDeviceStatus()
            CheckForCommands()
    except:
        print("TODO Handle errors here appropriately. Exit the program?")

if __name__ == "__main__":
    main()