import mysql.connector
import logging
from config_loader import ConfigLoader


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def db_connection():
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
