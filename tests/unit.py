# _author: Coke
# _date: 2022/8/15 14:23

import unittest
from application import create_app, socketio


class TestMyApp(unittest.TestCase):

    def setUp(self):

        build = 'local'
        app = create_app(build)
        socketio.run(app)
        self.client = app.test_client()

    def test_hello_world(self):
        response = self.client.post('/api/v1/client/user/login')
        print(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

    # def test_json_response(self):
    #     response = self.client.get('/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content_type, 'application/json')
    #     self.assertEqual(response.json, {'message': 'Hello, World!'})


if __name__ == '__main__':
    unittest.main()
