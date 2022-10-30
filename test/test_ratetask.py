import unittest

from application import create_app


class RateTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(True, '.envtest')
        self.client = self.app.test_client()
        self.app.testing = True

    def test_200(self):
        response = self.client.get('/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination'
                                   '=north_europe_main')
        assert response.status_code == 200

    def test_400(self):
        response = self.client.get('/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination'
                                   '=')
        assert response.status_code == 400


if __name__ == '__main__':
    unittest.main()
