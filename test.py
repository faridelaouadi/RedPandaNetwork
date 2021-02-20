from app import app
from unittest.mock import patch
import unittest

class FlaskTest(unittest.TestCase):
    
    #check if the index route redirects us 
    def test_index_route_redirect(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code,302)
    
        

if __name__ == "__main__":
    unittest.main()
