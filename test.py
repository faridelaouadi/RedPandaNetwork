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
    
    #test /home status code 200
    def test_home_route(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        status_code = response.status_code
        camera_list = response.camera_list
        self.assertEqual(status_code,200)

    #test /home content is html 

    #test /getCameraList is json and status code 200 and returns a non empty list 

    #test /getSightings is json , status code 200 and returns a non empty list 

    #test /camera_images/0010 is json , status code 200 and non empty list

    #test /camera_images/1010 is json , status code Fail

    #test getModifiedList using normal function unittest 

    #
    
        

if __name__ == "__main__":
    unittest.main()
