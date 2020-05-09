import os
from tabulate import tabulate


class Migration:
    def __init__(self, version, name, file):
        self.version = version
        self.name = name
        self.file = file

    def as_table(self):
        return [
            self.version,
            self.name,
            self.file
        ]


class ScriptsCollector():
    def __init__(self, migrations_path, rollbacks_path):
        self.migrations_path = migrations_path
        self.rollbacks_path = rollbacks_path

        self.migrations = self._collect_scripts(migrations_path)
        self.rollbacks = self._collect_scripts(rollbacks_path)

    def _get_metadata(self, file):
        migration_parts = os.path.splitext(file)[0].split("_", 1)
        version = migration_parts[0]
        name = migration_parts[1]\
            .replace("_", " ")\
            .capitalize()

        return Migration(
            version,
            name,
            file
        )

    def _collect_scripts(self, path):
        files = os.listdir(path)
        return (self._get_metadata(file) for file in files if file.endswith(".sql"))

    def _list_migrations(self, migrations):
        headers = ["Version", "Name", "File"]
        table = (migration.as_table() for migration in migrations)
        print(tabulate(table, headers, tablefmt="psql"))

    def list_migrations(self):
        self._list_migrations(self.migrations)

    def list_rollbacks(self):
        self._list_migrations(self.rollbacks)
