import argparse
from scriba import Scriba

parser = argparse.ArgumentParser()
file_path = "./migrations.yml"

parser.add_argument(
    "config",
    type=str,
    help="Scriba configurations file. Default: ./migrations.yml"
)

parser.add_argument(
    "action",
    type=str,
    help="Action to execute [status | migrate | rollback]"
)

# parser.add_argument(
#     "-s",
#     "--steps",
#     type=int,
#     help="Number of scripts to run"
# )

args = parser.parse_args()

if args.config:
    file_path = args.config

scriba = Scriba(file_path)

if args.action == "status":
    scriba.status()

if args.action == "migrate":
    scriba.migrate()

if args.action == "rollback":
    scriba.rollback()
