import logging
import argparse
import migrations_runner
from migrations_scanner import ScriptsCollector
from migrations_dao import MigrationsDao
from tabulate import tabulate

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

collector = ScriptsCollector()
migrations_dao = MigrationsDao()


def scan():
    """
    Looks for migration scripts and registers it into
    database migrations table

    :return:
    """
    migrations_dao.upsert(collector.migrations)


def status():
    scan()
    migrations = migrations_dao.find_all()
    headers = ["Version", "Name", "Status", "Status Update"]
    table = (migration.as_row() for migration in migrations)
    logger.info(tabulate(table, headers, tablefmt="psql"))


def migrate(steps=None):
    scan()
    if migrations_runner.migrate(migrations_dao, steps):
        status()


def rollback(steps=None):
    scan()
    if migrations_runner.rollback(collector, migrations_dao, steps):
        status()


parser = argparse.ArgumentParser()
parser.add_argument(
    "action",
    type=str,
    help="Action to execute: [status|migrate|rollback"
)
parser.add_argument(
    "-s",
    "--steps",
    type=int,
    help="Number of scripts to run"
)

args = parser.parse_args()
if args.action == "status":
    status()
if args.action == "migrate":
    migrate()
if args.action == "rollback":
    rollback()
