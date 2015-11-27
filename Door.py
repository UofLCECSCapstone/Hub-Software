#######################################################
# Door.py: Represents and provides functions for      #
# interacting with the doors the hub is connected to. #
#######################################################

from enum import Enum
import Database

class Door():
    """
    Represents a door, which has a unique
    ID and can be opened/closed.
    """

    ### Door table column indices. ###
    IX_DOOR_ID = 0
    IX_DOOR_OPEN_STATUS = 1

    def __init__(self, ID, OpenStatus):
        assert ID is not None
        assert OpenStatus is not None
        assert 0 <= OpenStatus.value <= 1

        self.ID = ID
        self.OpenStatus = OpenStatus

    @staticmethod
    def FromID(ID):
        conn = Database.get_connection()
        cursor = conn.cursor()

        # TODO What if in the database there's a value other than 1 or 0? How should we parse that?
        for door in cursor.execute('SELECT ID, blnOpen FROM Door'):
            if door[Door.IX_DOOR_ID] == ID:
                FoundDoor = Door(door[Door.IX_DOOR_ID],
                                 DoorOpenStatus.Closed if door[Door.IX_DOOR_OPEN_STATUS] == 0 else DoorOpenStatus.Open)
                conn.close()
                
                return FoundDoor

        conn.close()

        raise NotImplementedError("TODO This should really be a not found exception or similar.")



    def ToggleOpenStatus(self):
        """
        Changes this Door's open status in the database.
        If the door is currently known to be open, after this
        method it will be known as closed. And vice-versa.
        """

        assert self.ID is not None
        
        conn = Database.get_connection()
        cursor = conn.cursor()

        # TODO This method should probably also perform the actual opening, to keep all the logic in one place.
        if self.OpenStatus == DoorOpenStatus.Closed:
            # TODO Is SQL injection a problem here?
            cursor.execute("UPDATE Door " +
                           "SET blnOpen = 1 " +
                           "WHERE ID = " + str(self.ID))
            self.OpenStatus = DoorOpenStatus.Open
        elif self.OpenStatus == DoorOpenStatus.Open:
            cursor.execute("UPDATE Door " +
                           "SET blnOpen = 0 " +
                           "WHERE ID = " + str(self.ID))
            self.OpenStatus = DoorOpenStatus.Closed
        else:
            raise NotImplementedError("TODO Add this code.")
            conn.close()
            
        # Save the changes
        conn.commit()

        # TODO Have the "opened or closed" part of the return string be based on the action actually taken.
        conn.close()

class DoorOpenStatus(Enum):
    Closed = 0
    Open = 1

    def __str__(self):
        # TODO Relying on value here is nasty.
        if self.value == 0:
            return "Closed"
        elif self.value == 1:
            return "Open"
        else:
            raise NotImplementedError("TODO Add this code.")
