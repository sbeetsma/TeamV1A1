import psycopg2


#Heb voor het gemak voor nu een classje geschreven.
#Maar wees niet bang om te verbeteren/vervangen in de toekomst.



class PostgreSQLdb:
    """A PostgreSQL (relational) database.

    Attributes:
        host: the hostname the database is hosted at (presumably localhost in this usecase).
        database: the name of the database (rcmd for all the group members).
        user: the user the database belongs to according to pgadmin (presumably postgres).
        password: the database password.
        port: the port the database is hosted at (presumably 5432 if DB is hosted on windows machine).
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

    def _connect(self):
        """Connects to the database.
        Assings a connection object to self.connection."""
        self.connection = psycopg2.connect(
            host = self.host,
            database = self.database,
            user = self.user,
            password = self.password,
            port = self.port
        )

    def _summon_cursor(self):
        """Creates a cursor within the database.
        Assigns a cursor object to self.cursor."""
        self.cursor = self.connection.cursor()

    def _close_connection(self):
        """Closes the connection with the database.
        Sets self.connection to none."""
        self.connection.close()
        self.connection = None

    def _close_cursor(self):
        """Closes the cursor within the database.
        Sets self.cursor to none."""
        self.cursor.close()
        self.cursor = None

    def _bare_query(self, query: str, parameters: tuple = None):
        """Executes an SQL query in the database.
        Able to sanatize inputs with the parameters parameter.

        Args:
            query:
                The SQL query to execute.
                May contain '%s' in place of parameters to let psycopg2 automatically format them.
                The values to replace the %s's with can be passed with the parameters parameter.
            parameters: tuple containing parameters to replace the %s's in the query with."""
        if parameters == None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, parameters)

    def _fetch_query_result(self) -> list[tuple]:
        """Get the results from the most recent query.

        Returns:
            list containing a tuple for every row in the query result."""
        return self.cursor.fetchall()

    def _commit_changes(self):
        """Commits any changes made in queries."""
        self.connection.commit()

    def query(self, query: str, parameters: tuple = None, expect_return: bool = False, commit_changes: bool = False) -> list[tuple] or None:
        """Opens a connection to the DB, opens a cursor, executes a query, and closes everything again.
        Also retrieves query result or commits changes if relevant.

        Args:
            query:
                The SQL query to execute.
                May contain '%s' in place of parameters to let psycopg2 automatically format them.
                The values to replace the %s's with can be passed with the parameters parameter.
            parameters: tuple containing parameters to replace the %s's in the query with.
            expect_return: bool for wether the query should expect a return.
            commit_changes: bool for wether changes were made to the DB that need to be committed.

        Returns:
            if expect_return:
                list containing a tuple for every row in the query result.
            else:
                None"""
        self._connect()
        self._summon_cursor()
        self._bare_query(query, parameters)
        output = None
        if expect_return:
            output = self._fetch_query_result()
        if commit_changes:
            self._commit_changes()
        self._close_cursor()
        self._close_connection()
        return output

    def many_update_queries(self, query: str, data_list: list[tuple]): #DO NOT USE YET
        """Execute a single query that updates the DB with many different values without constantly opening/closing cursors/connections.

        Args:
            query:
                The SQL query to execute with every dataset in data_list.
                Must contain '%s' in place of parameters to let psycopg2 automatically format them.
                The values to replace the %s's with must be passed with the parameters parameter.
            data_list:
                list containing a tuple for every query that has to be excecuted."""
        self._connect()
        self._summon_cursor()
        self.cursor.executemany(query, data_list)
        self._commit_changes()
        self._close_cursor()
        self._close_connection()
