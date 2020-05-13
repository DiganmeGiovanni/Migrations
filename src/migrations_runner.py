"""
Implements functionality to run sql scripts for migrations
and rollbacks
"""
import logging
from datetime import datetime

import mysql.connector
from db_helper import db_connection
from migrations_scanner import ScriptsCollector
from migrations_dao import MigrationsDao, MigrationStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def migrate(migrations_dao, steps=None):
    """
    Run the non applied migrations

    :param migrations_dao: DAO for migrations
    :type migrations_dao: MigrationsDao
    :param steps: Optional value to limit the number of migrations to run
    :type steps: int
    :return:
    """
    migrations = migrations_dao.find_all_non_applied()
    if len(migrations) == 0:
        logger.info("There are not pending migrations to apply")
        return False

    conn = db_connection()
    counter = 0

    for migration in migrations:
        if steps is not None and counter > steps:
            break

        with open(migration.file_path, 'r') as file:
            sql = file.read()
            commands = sql.split(";")

        try:
            cursor = conn.cursor()
            for command in commands:
                try:
                    if command.strip() != "":
                        cursor.execute(command)
                except mysql.connector.Error as e:
                    logger.error("Something went wrong in migration '{}' for statement: '{}'".format(
                        migration.version,
                        command
                    ))

                    cursor.close()
                    conn.rollback()
                    conn.close()
                    return False

            cursor.close()
            conn.commit()

            migration.status = MigrationStatus.APPLIED
            migration.status_update = datetime.now()
            migrations_dao.save(migration)
        except mysql.connector.Error as e:
            conn.rollback()
            conn.close()
            migration.status = MigrationStatus.ERROR
            migration.status_update = datetime.now()
            migrations_dao.save(migration)

            logger.error("Something went wrong with migration {}: {}".format(
                migration.version,
                e
            ))
            return False

    conn.close()
    return True


def rollback(collector, migrations_dao, steps=None):
    """
    Run rollback scripts for migrations marked as applied in database
    table

    :param collector: Migrations collector
    :type collector: ScriptsCollector
    :param migrations_dao: DAO for migrations
    :type migrations_dao: MigrationsDao
    :param steps: Optional value to limit the number of migrations to rollback
    :type steps: int
    :return:
    """
    migrations = migrations_dao.find_all_applied()
    if len(migrations) == 0:
        logger.info("There are no migrations to rollback")
        return False

    conn = db_connection()
    counter = 0

    for migration in migrations:
        if steps is not None and counter > steps:
            break

        rollback_script = collector.get_rollback(migration.version)
        if rollback_script is None:
            logger.error("Rollback not found for {}".format(migration.version))
            conn.rollback()
            conn.close()
            return False

        with open(rollback_script.file_path, 'r') as file:
            sql = file.read()
            commands = sql.split(";")

        try:
            cursor = conn.cursor()
            for command in commands:
                try:
                    if command.strip() != "":
                        cursor.execute(command)
                except mysql.connector.Error as e:
                    logger.error("Something went wrong in rollback '{}' for statement: '{}'".format(
                        migration.version,
                        command
                    ))
                    logger.error(e)

                    cursor.close()
                    conn.rollback()
                    conn.close()
                    return False

            cursor.close()
            conn.commit()

            migration.status = MigrationStatus.REVERTED
            migration.status_update = datetime.now()
            migrations_dao.save(migration)
        except mysql.connector.Error as e:
            conn.rollback()
            conn.close()
            migration.status = MigrationStatus.ERROR
            migration.status_update = datetime.now()
            migrations_dao.save(migration)

            logger.error("Something wen wrong with rollback {}: {}".format(
                migration.version,
                e
            ))
            return False

    conn.close()
    return True
