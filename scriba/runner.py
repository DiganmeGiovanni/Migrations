import argparse
from scriba.scriba import Scriba


def _parse_args():
    parser = argparse.ArgumentParser()

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

    return parser.parse_args()


def main():
    args = _parse_args()
    file_path = "/opt/migrations.yml"

    if args.config:
        file_path = args.config

    scriba = Scriba(file_path)

    if args.action == "status":
        scriba.status()

    if args.action == "migrate":
        scriba.migrate(steps=args.steps)

    if args.action == "rollback":
        scriba.rollback(steps=args.steps)


if __name__ == "__main__":
    main()
