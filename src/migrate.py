from migrations_dao import MigrationsDao

# migrations_dao = MigrationsDao()
# migrations_dao.get_migrations()

from scripts_collector import ScriptsCollector

collector = ScriptsCollector("../data/up", "../data/down")
migrations = collector.list_migrations()
migrations = collector.list_rollbacks()
