"""
test custom Django management commands.
"""
# This import mocks the behavior of the database
# We need to be able to simulate whether the databse sends a response or not
from unittest.mock import patch

# One of the possible errors we may encounter when we connect to the database
from psycopg2 import OperationalError as Psycopg2Error

# Helpful function that calls a command by the name
# Allows us to call the command that we're testing
from django.core.management import call_command
# This is another error that may get thrown depending on \
# the stage of our start up
from django.db.utils import OperationalError
# This is the base test case that we will use to create our unit tests
# Important that we use SimpleTestCase bc we are just testing the behavior \
# of our db, so migrations or anything needed behind the scenes won't show up
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class Commandtests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting operational error"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
