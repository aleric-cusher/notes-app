import requests
import unittest

base_url = 'http://localhost:8000/api/v0/users/'


class UserTestCase(unittest.TestCase):
    def test_a_register_user(self):
        url = base_url + 'register/'
        headers = {'Content-Type': 'application/json'}
        data = {
            "username": "newTest",
            "password": "testpassword",
            "email": "okro@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        response = requests.post(url, json=data, headers=headers)
        resp_data = response.json()
        self.assertEqual(response.status_code, 201, resp_data)
        self.assertEqual(list(resp_data.keys()), ["access", "refresh"], resp_data)
    
    def test_b_login_user(self):
        url = base_url + 'login/'
        headers = {'Content-Type': 'application/json'}
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = requests.post(url, json=data, headers=headers)
        resp_data = response.json()
        self.assertEqual(response.status_code, 200, resp_data)
        self.assertEqual(list(resp_data.keys()), ["access", "refresh"], resp_data)


class CheckUsernameAvailabilityTestCase(unittest.TestCase):
    def test_username_available(self):
        url = base_url + 'username-available/'
        headers = {'Content-Type': 'application/json'}
        data = {
            "username": "newuser"
        }
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['detail'], 'Username available')
        self.assertEqual(response_data['available'], True)

    def test_username_not_available(self):
        url = base_url + 'username-available/'
        headers = {'Content-Type': 'application/json'}
        data = {
            "username": "admin"
        }
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['detail'], 'Username taken')
        self.assertEqual(response_data['available'], False)

if __name__ == '__main__':
    unittest.main()
