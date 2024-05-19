class ConnectionManager:
    def __init__(self):
        self.connections = []
        self.connection_types = {}  # Dictionnaire pour stocker les types de connexion

    def add_connection(self, start_block, end_block, connection_point):
        """
        Add a connection between two blocks with a specific connection point.

        Args:
            start_block: The block where the connection starts.
            end_block: The block where the connection ends.
            connection_point: The point of connection (tuple of coordinates).
        """
        # Vérifier si une connexion entre les mêmes blocs avec le même type de connexion existe déjà
        existing_connection = self.get_existing_connection(start_block, end_block)
        if existing_connection:
            # Si une connexion existe déjà, ne pas ajouter une nouvelle connexion
            print(f"Connection already exists between {start_block} and {end_block} with type {existing_connection[2]}")
            return

        # Ajouter la nouvelle connexion
        self.connections.append((start_block, end_block, connection_point))
        
        # Déterminer le type de connexion à partir du point de connexion
        connection_type = self.get_connection_type(connection_point)
        if connection_type:
            # Convertir le QPointF en tuple (x, y) pour l'utiliser comme clé hashable
            connection_point_tuple = (connection_point.x(), connection_point.y())
            # Ajouter le type de connexion au dictionnaire de types de connexion
            self.connection_types[(start_block, connection_point_tuple)] = connection_type

    def get_existing_connection(self, start_block, end_block):
        """
        Get an existing connection between two blocks.

        Args:
            start_block: The block where the connection starts.
            end_block: The block where the connection ends.

        Returns:
            The existing connection if found (start_block, end_block, connection_point), None otherwise.
        """
        for connection in self.connections:
            if connection[0] == start_block and connection[1] == end_block:
                return connection
        return None


    def remove_connection(self, start_block, end_block, connection_point):
        """
        Remove a connection between two blocks with a specific connection point.

        Args:
            start_block: The block where the connection starts.
            end_block: The block where the connection ends.
            connection_point: The point of connection (tuple of coordinates).
        """
        connection_tuple = (start_block, end_block, connection_point)
        if connection_tuple in self.connections:
            self.connections.remove(connection_tuple)
            if (start_block, connection_point) in self.connection_types:
                del self.connection_types[(start_block, connection_point)]

    def has_connection(self, start_block, end_block):
        """
        Check if there is a connection between two blocks.

        Args:
            start_block: The block where the connection starts.
            end_block: The block where the connection ends.

        Returns:
            True if there is a connection, False otherwise.
        """
        return (start_block, end_block) in self.connections

    def get_connection_type(self, connection_point):
        """
        Determine the type of connection (input or output) based on the position of the connection point.

        Args:
            connection_point: The QPointF object representing the connection point.

        Returns:
            The connection type ('input' or 'output').
        """
        x = connection_point.x()
        y = connection_point.y()

        # Determine the connection type based on the y-coordinate of the connection point
        if x == 180 and y == 25:
            return 'body_code'  # This corresponds to the 'body_code' connection point
        elif x == 180 and y == 75:
            return 'loop_exit'  # This corresponds to the 'loop_exit' connection point
        else:
            return None  # Unknown connection type

    def print_connections(self):
        """
        Print all existing connections in the work area.
        """
        for connection in self.connections:
            start_block, end_block, connection_point = connection
            print(f"Connection from {start_block} to {end_block} at {connection_point} ({self.get_connection_type(connection_point)})")