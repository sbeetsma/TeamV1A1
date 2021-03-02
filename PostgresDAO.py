import psycopg2


#Heb voor het gemak voor nu een classje geschreven.
#Maar wees niet bang om te verbeteren/vervangen in de toekomst.



class PostgreSQLdbError(Exception):
    """Custom exception to help diagnose problems with the relational DB."""
    def __init__(self, message: str = "There's a problem with the database"):
        """Ïnitialize class instance."""
        super().__init__(message)


class PostgreSQLdb:
    """A PostgreSQL (relational) database.

    Attributes:
        host: the hostname the database is hosted at (presumably localhost in this usecase).
        database: the name of the database (rcmd for all the group members).
        user: the user the database belongs to according to pgadmin (presumably postgres).
        password: the database password.
        port: the port the database is hosted at.
        connection: a psycopg2.extensions.cursor object that represents a connection to the database.
        cursor: a psycopg2.extensions.connection that represents a cursor in the database."""
    def __init__(self, host: str, database: str, user: str, password: str, port: str):
        """Initialize class instance.

        Args:
            host: the hostname the database is hosted at (presumably localhost in this usecase).
            database: the name of the database (rcmd for all the group members).
            user: the user the database belongs to according to pgadmin (presumably postgres).
            password: the database password.
            port: the port the database is hosted at.
            """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connects to the database.
        Assings a connection object to self.connection."""
        self.connection = psycopg2.connect(
            host = self.host,
            database = self.database,
            user = self.user,
            password = self.password,
            port = self.port
        )

    def summon_cursor(self):
        """Creates a cursor within the database.
        Assigns a cursor object to self.cursor."""
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """Closes the connection with the database.
        Sets self.connection to none."""
        self.connection.close()
        self.connection = None

    def close_cursor(self):
        """Closes the cursor within the database.
        Sets self.cursor to none."""
        self.cursor.close()
        self.cursor = None

    def query(self, query: str, parameters: tuple = None):
        """Executes an SQL query in the database.
        Able to sanatize inputs with the parameters parameter.

        Args:
            """
        if parameters == None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, parameters)

    def fetch_query_result(self) -> list:
        return self.cursor.fetchall()

    def commit_changes(self):
        self.connection.commit()



#TODO: Finish docstrings