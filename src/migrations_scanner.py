import os
from config_loader import ConfigLoader


class ScriptMetadata:
    def __init__(self, version, name, file_path):
        self.version=version
        self.name=name
        self.file_path=file_path


class ScriptsCollector:
    def __init__(self):
        config_loader = ConfigLoader()
        migrations_path = config_loader.get_migrations_path()

        self.migrations = self._collect_scripts(migrations_path['up'])
        self.rollbacks = self._collect_scripts(migrations_path['down'])

    def _get_metadata(self, path, file):
        migration_parts = os.path.splitext(file)[0].split("_", 1)
        version = migration_parts[0]
        name = migration_parts[1]\
            .replace("_", " ")\
            .capitalize()

        return ScriptMetadata(
            version=version,
            name=name,
            file_path=os.path.abspath(os.path.join(path, file))
        )

    def _collect_scripts(self, path):
        files = os.listdir(path)
        return [self._get_metadata(path, file) for file in files if file.endswith(".sql")]

    def get_rollback(self, version):
        for rollback_file in self.rollbacks:
            if rollback_file.version == version:
                return rollback_file

        return None
