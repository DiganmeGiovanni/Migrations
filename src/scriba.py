import logging
from migrations_scanner import ScriptsCollector
from migrations_dao import MigrationsDao
from tabulate import tabulate

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

migrations_dao = MigrationsDao()


def scan(silent_mode=True):
    """
    Looks for migration scripts and registers it into
    database migrations table

    :return:
    """

    collector = ScriptsCollector()

    for migration in collector.migrations:
        migrations_dao.upsert(migration)

    if not silent_mode:
        logger.info("{} migrations has been processed"
                    .format(len(collector.migrations)))


def status():
    scan()
    migrations = migrations_dao.get_migrations()
    headers = ["Version", "Name", "Status", "Status Update"]
    table = (migration.as_row() for migration in migrations)
    logger.info(tabulate(table, headers, tablefmt="psql"))


status()
