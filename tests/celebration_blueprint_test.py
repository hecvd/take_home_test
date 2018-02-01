import unittest
import urllib2
import os
from flask import Flask
from flask_testing import TestCase
from blueprints import celebration_blueprint


class CelebrationBlueprintTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.register_blueprint(celebration_blueprint.guest_list_page)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_server_is_up_and_running(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
