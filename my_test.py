from app import app, get_modified_lists
from unittest.mock import patch
import unittest


class FlaskTest(unittest.TestCase):
    
    #check if the index route redirects us 
    def test_index_route_redirect(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code,302)

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
        self.assertEqual(status_code,404)

    #test getModifiedList 
    def test_get_modified_list_no_changes(self):
        list_a = [1,2,3,4,5]
        list_b = [6,7,8,9,10]

        changes = ["p_0", "p_0", "np_1", "np_1"]

        modified_a, modified_b = get_modified_lists(list_a,list_b,changes)

        self.assertTrue(modified_a==list_a and list_b==modified_b) #no changes to the lists

    def test_get_modified_list_1_switch(self):
        list_a = [1,2,3,4,5]
        list_b = [6,7,8,9,10]

        changes = ["p_0"]

        modified_a, modified_b = get_modified_lists(list_a,list_b,changes)

        self.assertTrue(1 in modified_b) #the number 1 gets moved to the other list
    
    

if __name__ == "__main__":
    unittest.main()
