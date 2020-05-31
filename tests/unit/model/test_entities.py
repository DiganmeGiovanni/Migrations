from datetime import datetime
from model.entities import Migration, MigrationStatus


class TestMigration:

    def test_from_row(self):
        row = [
            1,
            'V45',
            'Test',
            MigrationStatus.APPLIED.value,
            datetime.now(),
            "file/path",
            "file_rollback/path"
        ]

        migration = Migration.from_row(row)
        assert migration.db_id == 1
        assert migration.version == 'V45'
        assert migration.name == "Test"
        assert migration.status == MigrationStatus.APPLIED
        assert migration.file_path == "file/path"
        assert migration.rollback_file_path == "file_rollback/path"

    def test_as_row(self):
        migration = Migration(
            1,
            "V1",
            "Create schema",
            MigrationStatus.PENDING,
            datetime.now(),
            "some/path",
            "some_other/path"
        )

        row = migration.as_row()
        assert len(row) == 4

        row = migration.as_row(include_id=True)
        assert len(row) == 5
        assert row[0] == 1
        assert row[3] == MigrationStatus.PENDING.value

        row = migration.as_row(include_id=True, include_paths=True)
        assert len(row) == 7
        assert row[0] == 1
        assert row[3] == MigrationStatus.PENDING.value
        assert row[5] == "some/path"
        assert row[6] == "some_other/path"
