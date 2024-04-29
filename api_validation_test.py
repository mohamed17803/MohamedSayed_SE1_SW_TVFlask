import unittest
from app import app, db

class APITestCase(unittest.TestCase):
        def setUp(self):
            self.app = app.test_client()
            self.app.testing = True
            with app.app_context():
                db.create_all()

        def tearDown(self):
            with app.app_context():
                db.session.remove()
                db.drop_all()

        def test_register_endpoint(self):
            # Test successful registration
            response = self.app.post('/register', data={
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpassword'
            })
            self.assertEqual(response.status_code, 302)  # Assuming it redirects to the login page

            # Test registration with existing user
            response = self.app.post('/register', data={
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpassword'
            })
            self.assertEqual(response.status_code, 200)  # Assuming it returns to the registration page with an error

        def test_login_endpoint(self):
            # First, create a user
            self.test_register_endpoint()

            # Test successful login
            response = self.app.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            })
            self.assertEqual(response.status_code, 302)  # Assuming it redirects to the home page

            # Test login with wrong credentials
            response = self.app.post('/login', data={
                'username': 'testuser',
                'password': 'wrongpassword'
            })
            self.assertEqual(response.status_code, 200)  # Assuming it returns to the login page with an error

if __name__ == '__main__':
        unittest.main()
    