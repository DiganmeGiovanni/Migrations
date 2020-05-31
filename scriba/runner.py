import argparse
from scriba import Scriba

parser = argparse.ArgumentParser()
file_path = "./migrations.yml"

parser.add_argument(
    "action",
    type=str,
    choices=['status', 'migrate', 'rollback'],
    help="Action to execute"
)

parser.add_argument(
    "--config",
    "-c",
    type=str,
    help="Scriba configurations file. Default: ./migrations.yml"
)

parser.add_argument(
    "--steps",
    "-s",
    type=int,
    help="Number of scripts to run"
)

args = parser.parse_args()

if args.config:
    file_path = args.config

scriba = Scriba(file_path)

if args.action == "status":
    scriba.status()

if args.action == "migrate":
    scriba.migrate(steps=args.steps)

if args.action == "rollback":
    scriba.rollback(steps=args.steps)
