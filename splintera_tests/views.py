import unittest
import mock
import splintera.views


class Tests(unittest.TestCase):

	def setUp(self):
		import os
		from django.test.utils import setup_test_environment
		setup_test_environment()
		self.fixture_0 = [['9', '/home/imran/Code/splintera-web/splintera/views.py', 'dashboard'], ['9', '/home/imran/Code/splintera-web/splintera/views.py', 'dashboard']]

	@mock.patch('__builtin__.open')
	@mock.patch('urllib2.urlopen')
	@mock.patch('MySQLdb.connect')
	@mock.patch('django.contrib.auth.decorators.login_required', lambda x: x)
	@mock.patch('splintera.views.simple')
	@mock.patch('django.shortcuts.render_to_response')
	def test_dashboard(self,mock_render_to_response,mock_simple,mock_MySQLdb,mock_urllib2,mock_open):
		mock_MySQLdb.connect.return_value.cursor.return_value.execute.return_value = 1
		mock_MySQLdb.connect.return_value.cursor.return_value.fetchall.return_value = self.fixture_0
		mock_simple.return_value = [4]
		request_value = FilteredObject('other')
		result = splintera.views.dashboard(request=request_value)
		self.assertEqual(result,FilteredObject('other'))

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()
