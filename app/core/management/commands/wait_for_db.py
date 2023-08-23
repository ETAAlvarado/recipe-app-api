"""
Django command to wait for the database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        # This line logs a mesage to the screen saying we're waiting for the \
        # database
        self.stdout.write('Waiting for database...')
        # We then writing a bool storing false, since we're assuming the db \
        # is not up until it is
        db_up = False
        while db_up is False:
            try:
                # Here, we check the db and if it isn't ready, then it \
                # throws up an exception (line 26)
                self.check(databases=['default'])
                # Once we get to this line, the while loop stops
                db_up = True
            # This line raises an error depending on where in the db start \
            # the operation is currently stuck in
            # We know that if we get these exceptions, the db isn't ready \
            # yet since the db is on
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
