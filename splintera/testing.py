import unittest
import mock
import os
#from mock import patch
#from mock import create_autospec
#mock_function = create_autospec(function, return_value='fishy')
#but how do i monkeypatch the function called inside another function?  use the 'patch' decorator
#@patch('module.ClassName2')
#

class TestUM(unittest.TestCase):

    def setUp(self):
        #self.patcher1 = patch('testing.original_call',mocked_original_call)
        #self.MockClass1 = self.patcher1.start()
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        from django.test.utils import setup_test_environment
        setup_test_environment()
        pass

    @mock.patch('django.shortcuts.render_to_response')
    @mock.patch('MySQLdb.connect')
    def test_dashboard(self, mock_database,mock_response):
        mock_database.return_value.cursor.return_value.fetchall.return_value = [[1, 'C:/some_file', 'function_name']]
        #print mdb.connect().cursor().fetchall()
        request = {}
        import views
        views.dashboard(request)
        mock_response.assert_called_with('dashboard.html', {'traces': [[1, 'C:/some_file/function_name']]})
        #self.assertEqual(dbase(),)

    def tearDown(self):
        #self.patcher1.stop()
        pass

if __name__ == '__main__':
    unittest.main()