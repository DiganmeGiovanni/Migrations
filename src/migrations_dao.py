"""
Provides utilities to connect and retrieve/update database
records from migrations tracking table
"""
from datetime import datetime

import mysql.connector
import logging
from config_loader import ConfigLoader
from migrations_scanner import ScriptMetadata
from enum import Enum

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MigrationStatus(Enum):
    PENDING = "Pending"
    APPLIED = "Applied"
    ERROR = "Error"
    REVERTED = "Reverted"


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

    @staticmethod
    def from_row(row):
        return Migration(
            db_id=row[0],
            version=row[1],
            name=row[2],
            status=MigrationStatus(row[3]),
            status_update=row[4],
            file_path=row[5]
        )

    def as_row(self, include_id=False, include_path=False):
        row = []

        if include_id:
            row.append(self.db_id)

        row.extend([
            self.version,
            self.name,
            self.status.value,
            self.status_update
        ])

        if include_path:
            row.append(self.file_path)

        return row


class MigrationsDao:
    def __init__(self):
        self._MIGRATIONS_TABLE = "migrations"
        self._COL_ID = "id"
        self._COL_VERSION = "version"
        self._COL_NAME = "name"
        self._COL_STATUS = "status"
        self._COL_STATUS_UPDATE = "status_update"
        self._COL_FILE_PATH = "file_path"

        self._conn = self._get_connection()
        self._verify_table()

    def destroy(self):
        self._conn.close()

    def upsert(self, metadata_list):
        """
        Updates or inserts a list  metadata files as migration objects

        :param metadata_list: Migration files to process
        :type metadata_list: list[ScriptMetadata]
        """

        for metadata in metadata_list:
            migration = self.find_by_version(metadata.version)

            if not migration:
                migration = Migration(
                    version=metadata.version,
                    status=MigrationStatus.PENDING,
                    status_update=datetime.now()
                )

            migration.name = metadata.name
            migration.file_path = metadata.file_path
            self.save(migration)

    def save(self, migration):
        cursor = self._conn.cursor()
        db_migration = self.find_by_version(migration.version)

        if db_migration:
            query = """
                UPDATE {} SET 
                    name='{}',
                    status='{}',
                    status_update='{}',
                    file_path='{}'
                WHERE {} = '{}'
            """

            cursor.execute(query.format(
                self._MIGRATIONS_TABLE,
                migration.name,
                migration.status.value,
                migration.status_update.strftime("%Y-%m-%d %H:%M:%S"),
                migration.file_path,
                self._COL_VERSION,
                migration.version
            ))
        else:
            query = """
                INSERT INTO {} VALUES(
                    NULL,
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}'
                )
            """
            cursor.execute(query.format(
                self._MIGRATIONS_TABLE,
                migration.version,
                migration.name,
                migration.status.value,
                migration.status_update.strftime("%Y-%m-%d %H:%M:%S"),
                migration.file_path
            ))

        cursor.close()
        self._conn.commit()

    def find_all(self):
        query = "SELECT * FROM {} ORDER BY {}"

        cursor = self._conn.cursor()
        cursor.execute(query.format(
            self._MIGRATIONS_TABLE,
            self._COL_VERSION
        ))

        return [Migration.from_row(row) for row in cursor.fetchall()]

    def find_by_version(self, version):
        cursor = self._conn.cursor()

        query = "SELECT * FROM {} WHERE {} = '{}' LIMIT 1"
        cursor.execute(query.format(
            self._MIGRATIONS_TABLE,
            self._COL_VERSION,
            version
        ))

        db_migration = cursor.fetchone()
        cursor.close()

        if db_migration:
            return Migration.from_row(db_migration)

        return None

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
