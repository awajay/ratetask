import unittest

from application import create_app


class RateFailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(True, '.envfailtest')
        self.client = self.app.test_client()
        self.app.testing = True

    def test_500(self):
        response = self.client.get('/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination'
                                   '=test1')
        print(response)
        assert response.status_code == 500


if __name__ == '__main__':
    unittest.main()
