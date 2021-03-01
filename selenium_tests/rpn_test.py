import unittest
from selenium import webdriver
import page
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json 
import requests

class RedPandaNetworkApp(unittest.TestCase):

    def setUp(self):
        #everytime we run a test we need to log in using MSFT
        self.driver = webdriver.Chrome("/Users/farid/Desktop/chromedriver")
        self.driver.maximize_window()
        self.driver.get("https://redpandanetwork.azurewebsites.net/")
        MSFTLogin = page.MSFTLogin(self.driver)
        MSFTLogin.login()

    def test_login_works(self):
        #Load the main page. In this case the home page of Python.org.
        main_page = page.MainPage(self.driver)
        #Checks if the word "Python" is in title
        assert main_page.is_title_matches(), "Red panda network dashboard title doesn't match."
    
    def test_add_camera(self):
        main_page = page.MainPage(self.driver)
        assert main_page.click_add_camera(), "Add Camera Modal is not popping up"
    
    def test_add_camera_ID_already_exists(self):
        main_page = page.MainPage(self.driver)
        assert main_page.add_new_camera("0010") == False #alert showed up
    
    def test_add_camera_ID_valid(self):
        main_page = page.MainPage(self.driver)
        assert main_page.add_new_camera("0016") == True #alert showed up

    def test_go_to_upload_page(self):
        main_page = page.MainPage(self.driver)
        main_page.toggle_menu()
        main_page.change_to_upload_page()
        assert "upload" in self.driver.current_url

    def test_upload_image_to_camera(self):
        main_page = page.MainPage(self.driver)
        main_page.toggle_menu()
        main_page.change_to_upload_page()
        #now on the upload page 
        #get the number of images for 0015 
        number_of_current_images = len(json.loads((requests.get('https://redpandanetwork.azurewebsites.net/camera_images/0015')).text)['urls'])
        #add an image
        main_page.upload_image()
        number_of_new_images = len(json.loads((requests.get('https://redpandanetwork.azurewebsites.net/camera_images/0015')).text)['urls'])
        assert number_of_current_images + 1 == number_of_new_images

    def test_drag_and_drop(self):
        number_of_false_positives = [i[1] for i in json.loads((requests.get('https://redpandanetwork.azurewebsites.net/camera_images/0015')).text)['urls']].count(False)
        main_page = page.MainPage(self.driver)
        main_page.toggle_menu()
        main_page.change_to_upload_page()
        main_page.drag_and_drop()
        number_of_new_false_positives = [i[1] for i in json.loads((requests.get('https://redpandanetwork.azurewebsites.net/camera_images/0015')).text)['urls']].count(False)
        assert number_of_false_positives + 1 == number_of_new_false_positives

    def test_panda_sighting_upload(self):
        number_of_panda_sightings = len(json.loads((requests.get('https://redpandanetwork.azurewebsites.net/getSightings')).text)['sightings_list'])
        main_page = page.MainPage(self.driver)
        main_page.toggle_menu()
        main_page.change_to_upload_page()
        main_page.add_panda_sighting()
        number_of_new_panda_sightings = len(json.loads((requests.get('https://redpandanetwork.azurewebsites.net/getSightings')).text)['sightings_list'])
        assert number_of_panda_sightings + 1 == number_of_new_panda_sightings

    def test_camera_click(self):
        main_page = page.MainPage(self.driver)
        assert main_page.camera_click() == True
    
    def test_panda_click(self):
        main_page = page.MainPage(self.driver)
        assert main_page.panda_sighting_click() == True
        
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()