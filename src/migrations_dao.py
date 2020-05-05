"""
Provides utilities to connect and retrieve/update database
records from migrations tracking table
"""

import mysql.connector
import logging
from config_loader import ConfigLoader

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MigrationsDao:
    def __init__(self):
        self.conn = self._get_connection()

    def destroy(self):
        self.conn.close()

    def get_migrations(self):
        self._verify_table('migrations')
        query = "SELECT * FROM migrations"
        # run query

    def _verify_table(self, table):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{}'
        """.format(table))

        if cursor.fetchone()[0] == 1:
            cursor.close()
            print("Table exists")
            return True

        # Create table
        cursor.close()
        print("Table not found")
        return False

    @staticmethod
    def _get_connection():
        config_loader = ConfigLoader()
        connection = None

        try:
            datasource = config_loader.get_datasource()

            connection = mysql.connector.connect(
                host=datasource['host'],
                user=datasource['username'],
                passwd=datasource['password'],
                database=datasource['database']
            )

        except mysql.connector.Error as e:
            logger.error("Error during connection: {}".format(e))

        return connection
