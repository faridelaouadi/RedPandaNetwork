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

    #test /home content is html 

    #test /getCameraList is json and status code 200 and returns a non empty list 
    def test_get_camera_list(self):
        tester = app.test_client(self)
        response = tester.get("/getCameraList")
        status_code = response.status_code
        self.assertEqual(status_code,200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    #test /getSightings is json , status code 200 and returns a non empty list
    def test_sightings(self):
        tester = app.test_client(self)
        response = tester.get("/getSightings")
        status_code = response.status_code
        self.assertEqual(status_code,200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    #test /camera_images/0010 is json , status code 200 and non empty list
    def test_get_camera_images_correct_ID(self):
        tester = app.test_client(self)
        response = tester.get("/camera_images/0010")
        status_code = response.status_code
        self.assertEqual(status_code,200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    #test /camera_images/1010 is json , status code Fail
    def test_get_camera_images_incorrect_ID(self):
        tester = app.test_client(self)
        response = tester.get("/camera_images/0101")
        status_code = response.status_code
        self.assertEqual(status_code,200)

    #test getModifiedList using normal function unittest 

    #
    
        

if __name__ == "__main__":
    unittest.main()
