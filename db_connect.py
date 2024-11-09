import os
import psycopg2

import Logger

HOST = "192.168.2.213" 
#HOST = "127.0.0.1" 
DATABASE = "postgres"
USER = "admin"
PASSWORD = "admin"
resetDBOnStartup = False  # TODO: set False in production

def read_file(filepath):
    with open(filepath, "r") as file:
        return file.read()
    
class dbManager:
    def __init__(self, logger) -> None:
        try:
            self.logger = logger
            # Connect to the PostgreSQL server
            connection = psycopg2.connect(
                host=HOST,
                database=DATABASE,
                user=USER,
                password=PASSWORD
            )
            self.cursor = connection.cursor()
            self.conn = connection
            logger.info("Succeeded to connect to PostgreSQL database")
            
        except Exception as error:
            logger.error("Error while connecting to PostgreSQL:", error)
            exit(1)
        
        if not self.check_for_database_content() or resetDBOnStartup:
            self.init_database()
            
    def init_database(self):
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        self.logger.error("Database initialization aborted")
        # self.logger.debug("init_database is called")
        # self.logger.info("Initializing database...")
        # query = "DROP SCHEMA public CASCADE;CREATE SCHEMA public;"
        # self.logger.debug(f"executing SQL query: {query}")
        # self.cursor.execute(query)
        # self.logger.warn("Database dropped")
        # self.conn.commit()
        
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # filepath = os.path.join(current_dir, "sql", "init.sql")
        # query = read_file(filepath)
        # self.logger.debug(f"executing SQL query: {query}")
        # try:
        #     self.cursor.execute(query)
        #     self.conn.commit()
        #     self.logger.info("Tables initiated successfully")
        #     self.populate_database()
        # except Exception as e:
        #     self.logger.error(f"Error creating tables: {e}")
        #     self.conn.rollback()
        #     return False
        return True
    def get_all_tables(self):
        """
        Retrieves all table names from the connected database.

        Parameters:
        None

        Returns:
        tables (list): A list of tuples, where each tuple contains one table name.
        """
        self.logger.debug("get_all_tables is called")
        query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema');"
        self.logger.debug(f"executing SQL query: {query}")
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        self.logger.debug(f"Table names retrieved: {tables}")
        return tables

    def check_for_database_content(self):
        self.logger.debug("check_for_database_content is called")
        actual_table_count = len(self.get_all_tables())
        if actual_table_count < 1:
            self.logger.debug(f"Database not initialized yet")
            return False
        else:
            self.logger.debug("Database already initialized.")
        return True
    
    def populate_database(self):
        self.add_user("admin", "sicherheit")

    def add_user(self, username, password):
        self.logger.debug("add_user is called")        
        """
        Adds a new user to the 'user' table.
        
        :param username: Username of the user
        :param password: Password of the user 
        """
        try:
            query = """
                INSERT INTO "user" (username, "password")
                VALUES (%s, %s);
            """
            data = (username, password)
            self.logger.debug(f"executing SQL query: {query}")
            self.logger.debug(f"with data: {data}")

            self.cursor.execute(query, data)
            self.conn.commit()
            return True
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            self.logger.error(f"Error adding user: {e}")
            return False
        
    def modify_entry(self, user_id, field_id):
        try:
            query = """
                    SELECT toggle_assigned_id(%s, %s);
                    """
            data = (user_id, field_id)
            self.logger.debug(f"executing SQL query: {query}")
            self.logger.debug(f"with data: {data}")
            self.cursor.execute(query, data)
            self.conn.commit()
            return True
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            self.logger.error(f"Error adding user: {e}")
            return False
    
    def get_entries_by_user_id(self, user_id):
        self.logger.debug("get_entries_by_user_id is called")
        query = "SELECT assigned_id FROM user_ids WHERE user_id = %s;"
        self.logger.debug(f"executing SQL query: {query} with user_id: {user_id}")
        
        try:
            self.cursor.execute(query, (user_id,))
            entries = self.cursor.fetchall()
            self.logger.info(f"Retrieved entries for user_id {user_id}: {entries}")
            return [item[0] for item in entries]
        except Exception as e:
            self.logger.error(f"Error retrieving entries for user_id {user_id}: {e}")
            return None
    
    def view_all(self): # beta
        self.logger.debug("view_all is called")
        query = """
                SELECT assigned_id, COUNT(*) AS frequency
                FROM user_ids
                GROUP BY assigned_id
                ORDER BY frequency DESC;
                """    
        self.logger.debug(f"executing SQL query: {query}")
        try:
            self.cursor.execute(query)
            entries = self.cursor.fetchall()
            self.logger.info(f"Retrieved entries: {entries}")
            return entries
        except Exception as e:
            self.logger.error(f"Error retrieving entries: {e}")
            return None
        
    def view_all2(self, max_frequency=None):  # max_frequency is an optional parameter
        self.logger.debug("view_all is called with max_frequency=%s", max_frequency)
        
        # Base query
        query = """
                SELECT assigned_id, COUNT(*) AS frequency
                FROM user_ids
                WHERE user_id IN (
                    SELECT user_id
                    FROM user_ids
                    GROUP BY user_id
                    HAVING COUNT(*) <= %s
                )
                GROUP BY assigned_id
                ORDER BY frequency DESC;
                """
        
        
        self.logger.debug(f"Executing SQL query: {query}")
        
        try:
            self.cursor.execute(query, (max_frequency if max_frequency else 999,))
            entries = self.cursor.fetchall()
            self.logger.info(f"Retrieved entries: {entries}")
            return entries
        except Exception as e:
            self.logger.error(f"Error retrieving entries: {e}")
            return None

    
    def getTotalVotes(self, max_frequency=None):
        query = """SELECT COUNT(*)
FROM user_ids
WHERE user_id IN (
    SELECT user_id
    FROM user_ids
    GROUP BY user_id
    HAVING COUNT(*) <= %s
);
"""
        self.logger.debug(f"executing SQL query: {query}")
        try:
            self.cursor.execute(query, (max_frequency if max_frequency else 999,))
            total_votes = self.cursor.fetchone()[0]
            self.logger.info(f"Retrieved total votes: {total_votes}")
            return total_votes
        except Exception as e:
            self.logger.error(f"Error retrieving total votes: {e}")
            return None
        
    def getStudentCount(self, max_frequency=None):
        query = """SELECT COUNT(DISTINCT user_id)
FROM user_ids
WHERE user_id IN (
    SELECT user_id
    FROM user_ids
    GROUP BY user_id
    HAVING COUNT(*) <= %s
);
"""
        self.logger.debug(f"executing SQL query: {query}")
        try:
            self.cursor.execute(query, (max_frequency if max_frequency else 999,))
            total_votes = self.cursor.fetchone()[0]
            self.logger.info(f"Retrieved student count: {total_votes}")
            return total_votes
        except Exception as e:
            self.logger.error(f"Error retrieving student count: {e}")
            return None

    def getMostFrequentStudentCount(self, max_frequency=None):
        query = """
            SELECT user_id, COUNT(*) AS frequency
FROM user_ids
WHERE user_id IN (
    SELECT user_id
    FROM user_ids
    GROUP BY user_id
    HAVING COUNT(*) <= %s
)
GROUP BY user_id
ORDER BY frequency DESC
LIMIT 1;

        """
        self.logger.debug(f"Executing SQL query: {query}")
        try:
            self.cursor.execute(query, (max_frequency if max_frequency else 999,))
            result = self.cursor.fetchone()
            most_frequent_user_id, highest_count = result[0], result[1]
            self.logger.info(f"Most frequent user_id: {most_frequent_user_id}, Count: {highest_count}")
            return highest_count
        except Exception as e:
            self.logger.error(f"Error retrieving most frequent student count: {e}")
            return None

    def getIgnoredStudents(self, max_frequency):
        query = """SELECT COUNT(*) AS ignored_users_count
FROM (
    SELECT user_id
    FROM user_ids
    GROUP BY user_id
    HAVING COUNT(*) > %s
) AS ignored_users;
"""
        self.logger.debug(f"Executing SQL query: {query}")
        try:
            self.cursor.execute(query, (max_frequency if max_frequency else 999,))
            ignored = self.cursor.fetchone()[0]
            return ignored
        except Exception as e:
            self.logger.error(f"Error retrieving most frequent student count: {e}")
            return None