from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available."""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Whenever this is called, it's overwritten with mock object,
            # always returning True,
            # and you are able to monitor number of times the function
            # was called, etc.
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # Using as a decorator does the same as a with-command
    # You need to add it as an extra argument (ts in this case)
    # time.sleep will now just return true, hence not actually sleeping
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db."""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Function will raise OperationalError 5 times,
            # and not anymore on 6th time
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
