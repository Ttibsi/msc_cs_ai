"""_summary_

"""
class User:
    """_summary_
    """
    def __init__(self, user_id, name):
        """Construct an instance of User.

        Args:
            user_id (str): he unique identifier of the user
            name (str): the name of the user
        """
        self._id = user_id
        self._name = name
        self._connections = set()

    def get_id(self):
        """Return the unique identifier of the user instance.

        Returns:
            str: the unique identifier of the user instance.
        """
        return self._id

    def get_name(self):
        """Return the name of the user.

        Returns:
            str: the name of the user.
        """
        return self._name

    def get_connections(self):
        """Returns the set of connections of the user, i.e., the set of user unique
        identifiers with whom the user has a connection.

        Returns:
            set: the set of unique identifiers of users with whom he/she has a connection.
        """
        return self._connections

    def add_connection(self, user_id):
        """Add a connection to the user's circle. Return true if the operation is
        successful, false otherwise (if the user is already part of his/her circle of connections).

        Args:
            user_id (str): the user id to be added to this instance set of connections.
        Returns:
            bool: True if the operation is successful, False otherwise 
            (e.g., user_id already in the set of connections).
        """
        if user_id not in self._connections:
            self._connections.add(user_id)
            return True
        else:
            return False

    def remove_connection(self, user_id):
        """
        Remove a connection from the user's circle. Return true if the operation is
        successful, false otherwise (if the user is not part of his/her circle of connections).

        Args:
            user_id (str): the user id to be removed from this instance set of connections.
        
        Returns:
            bool: True if the operation is successful, False otherwise 
            (e.g., user_id is not in the set of connections).
        """
        return self._connections.discard(user_id) is not None

    def __eq__(self, other):
        if isinstance(other, User):
            return self._id == other._id and self._name == other._name
        return NotImplemented
