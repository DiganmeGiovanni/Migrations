import os
from migrations_dao import Migration
from config_loader import ConfigLoader


class ScriptsCollector:
    def __init__(self):
        config_loader = ConfigLoader()
        migrations_path = config_loader.get_migrations_path()

        self.migrations = self._collect_scripts(migrations_path['up'])
        self.rollbacks = self._collect_scripts(migrations_path['down'])

    def _get_metadata(self, file):
        migration_parts = os.path.splitext(file)[0].split("_", 1)
        version = migration_parts[0]
        name = migration_parts[1]\
            .replace("_", " ")\
            .capitalize()

        return Migration(
            version=version,
            name=name,
            file_path=os.path.abspath(file)
        )

    def _collect_scripts(self, path):
        files = os.listdir(path)
        return [self._get_metadata(file) for file in files if file.endswith(".sql")]
