import os
import config_loader
from unittest.mock import patch
from migrations_processors.scanners import FileScanner, ScriptMetadata

test_data_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "data",
)


class TestFileScanner:

    @patch('config_loader.ConfigLoader')
    def test_scan(self, conf_loader_mocker):
        conf_loader_mocker.return_value.get_migrations_path.return_value = {
            'up': os.path.join(test_data_path, "up"),
            'down': os.path.join(test_data_path, "down")
        }

        # Given
        mock_conf_loader = config_loader.ConfigLoader("test")
        scanner = FileScanner(mock_conf_loader)

        # When
        migrations_metadata = scanner._scan()

        # Then
        assert len(migrations_metadata) == 2
        for meta in migrations_metadata:
            assert type(meta) is ScriptMetadata

    @patch('config_loader.ConfigLoader')
    def test_parse_name(self, conf_loader_mocker):
        # Verify class was mocked successfully
        assert conf_loader_mocker == config_loader.ConfigLoader

        mock_conf_loader = config_loader.ConfigLoader("test")
        scanner = FileScanner(mock_conf_loader)

        file = "V4.5_Create_schema.sql"
        version, name = scanner._parse_name(file)
        assert version == 'V4.5'
        assert name == "Create schema"

    @patch('config_loader.ConfigLoader')
    @patch('os.listdir')
    def test_find_rollback(self, listdir_mocker, conf_loader_mocker):
        down_path = os.path.join(test_data_path, "down")
        conf_loader_mocker.return_value.get_migrations_path.return_value = {
            'up': os.path.join(test_data_path, "up"),
            'down': down_path
        }

        listdir_mocker.return_value = [
            'V1_Create_tables.sql',
            'V1.1_Add_tables.sql',
            'V2_Add_foreign_keys.sql',
            'V3_Add_last_table.sql'
        ]

        mock_conf_loader = config_loader.ConfigLoader("test")
        scanner = FileScanner(mock_conf_loader)

        rollback_path = scanner._find_rollback("V1")
        assert rollback_path == os.path.abspath(os.path.join(
            down_path,
            "V1_Create_tables.sql"
        ))

        rollback_path = scanner._find_rollback("V3")
        assert rollback_path == os.path.abspath(os.path.join(
            down_path,
            "V3_Add_last_table.sql"
        ))
