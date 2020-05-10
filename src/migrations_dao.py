"""
Provides utilities to connect and retrieve/update database
records from migrations tracking table
"""

import mysql.connector
import logging
from config_loader import ConfigLoader

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Migration:
    def __init__(
            self,
            db_id=None,
            version=None,
            name=None,
            status=None,
            status_update=None,
            file_path=None):
        """
        Represents each migration and its status

        :param db_id: Id will be provided by database
        :param version: Parsed version number from file name
        :param name: Name parsed from file name
        :param status: Status of migration
        :param status_update: Timestamps when the status was updated
        :param file_path: Absolute file path to script file
        """

        self.db_id = db_id
        self.version = version
        self.name = name
        self.status = status
        self.status_update = status_update
        self.file_path = file_path

    def as_row(self, include_id=False, include_path=False):
        row = []

        if include_id:
            row.append(self.db_id)

        row.extend([
            self.version,
            self.name,
            self.status,
            self.status_update
        ])

        if include_path:
            row.append(self.file_path)

        return row


class MigrationsDao:
    def __init__(self):
        self._conn = self._get_connection()
        self._MIGRATIONS_TABLE = "migrations"

        self._COL_ID = "id"
        self._COL_VERSION = "version"
        self._COL_NAME = "name"
        self._COL_STATUS = "status"
        self._COL_STATUS_UPDATE = "status_update"
        self._COL_FILE_PATH = "file_path"

    def destroy(self):
        self._conn.close()

    def get_migrations(self):
        if self._is_table_created():
            query = "SELECT * FROM migrations ORDER BY {}"\
                .format(self._COL_VERSION)

            cursor = self._conn.cursor()
            cursor.execute(query)
            db_migrations = cursor.fetchall()

            migrations = []
            for db_migration in db_migrations:
                row = list(db_migration)
                migrations.append(Migration(
                    db_id=row[0],
                    version=row[1],
                    name=row[2],
                    status=row[3],
                    status_update=row[4],
                    file_path=row[5]
                ))

            return migrations

        else:
            logger.warning("Migrations table not found")
            return []

    def upsert(self, migration):
        self._verify_table()
        cursor = self._conn.cursor()

        if self._is_migration_registered(migration.version):
            query = "UPDATE {} SET name='{}', file_path='{}' WHERE {} = '{}'"
            cursor.execute(query.format(
                self._MIGRATIONS_TABLE,
                migration.name,
                migration.file_path,
                self._COL_VERSION,
                migration.version
            ))
        else:
            query = "INSERT INTO {} VALUES (NULL, '{}', '{}', '{}', NOW(), '{}')"
            cursor.execute(query.format(
                self._MIGRATIONS_TABLE,
                migration.version,
                migration.name,
                "PENDING",  # TODO Use enum python equivalent
                migration.file_path
            ))

        self._conn.commit()
        cursor.close()

    def _is_migration_registered(self, version):
        cursor = self._conn.cursor()

        query = "SELECT COUNT(*) FROM {} WHERE {} = '{}'"
        cursor.execute(query.format(
            self._MIGRATIONS_TABLE,
            self._COL_VERSION,
            version
        ))

        migration_exists = cursor.fetchone()[0] == 1
        cursor.close()
        return migration_exists

    def _verify_table(self):
        if not self._is_table_created():
            self._create_table()

    def _is_table_created(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{}'
        """.format(self._MIGRATIONS_TABLE))

        table_exists = cursor.fetchone()[0] == 1

        cursor.close()
        return table_exists

    def _create_table(self):
        query = """
            CREATE TABLE {}(
                {} INTEGER PRIMARY KEY AUTO_INCREMENT,
                {} VARCHAR(500) NOT NULL,
                {} VARCHAR(1000) NOT NULL,
                {} VARCHAR(255) NOT NULL,
                {} DATETIME NOT NULL DEFAULT NOW(),
                {} VARCHAR(3000) NOT NULL
            )
        """.format(
            self._MIGRATIONS_TABLE,
            self._COL_ID,
            self._COL_VERSION,
            self._COL_NAME,
            self._COL_STATUS,
            self._COL_STATUS_UPDATE,
            self._COL_FILE_PATH
        )

        try:
            cursor = self._conn.cursor()
            cursor.execute(query)
            cursor.close()
        except mysql.connector.Error as e:
            logger.error("'{}' table could not be created {}"
                         .format(self._MIGRATIONS_TABLE, e))

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
