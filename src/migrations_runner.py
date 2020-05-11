"""
Implements functionality to run sql scripts for migrations
and rollbacks
"""


def migrate(steps=None):
    """
    Run the non applied migrations

    :param steps: Optional value to limit the number of migrations to run
    :type steps: int
    :return:
    """
    pass


def rollback(steps=None):
    """
    Run rollback scripts for migrations marked as applied in database
    table

    :param steps: Optional value to limit the number of migrations to rollback
    :type steps: int
    :return:
    """
