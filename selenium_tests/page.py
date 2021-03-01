
from locators import MainPageLocators, LoginPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""
    def __init__(self, driver):
        self.driver = driver

class MainPage(BasePage):

    def is_title_matches(self):
        """Verifies that the hardcoded text "Python" appears in page title"""
        return "Welcome" in self.driver.title
    
    def click_add_camera(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ADD_CAMERA_BUTTON)).click() #press the add camera button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ADD_CAMERA_BUTTON_WITHIN_MODAL))
        return "show" in self.driver.find_element_by_id('editCamerasModal').get_attribute("class") #the pop up modal is shown 

    def add_new_camera(self,id):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ADD_CAMERA_BUTTON)).click() #press the add camera button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ADD_CAMERA_PROPOSED_CAMERA_ID)).send_keys(id)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ADD_CAMERA_LATITUDE)).send_keys("10")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ADD_CAMERA_LONGITUDE)).send_keys("10")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ADD_CAMERA_BUTTON_WITHIN_MODAL)).click()
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            valid = False
        except TimeoutException:
            valid = True
        return valid
    
    def toggle_menu(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.TOGGLE_MENU)).click()
    
    def change_to_upload_page(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.UPLOAD_PAGE_LINK)).click()

    def upload_image(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.CAMERA_0015_CHECKBOX)).click() #choose camera 0015 checkbox
        self.driver.find_element_by_xpath("//input[@type='file' and @form='upload_images_form']").send_keys(os.getcwd()+"/redpanda.jpg")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ANALYSE_IMAGES_BUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.UPLOAD_IMAGES_BUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.CAMERA_0015_CHECKBOX))

    def drag_and_drop(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.CAMERA_0015_CHECKBOX)).click() #choose camera 0015 checkbox
        self.driver.find_element_by_xpath("//input[@type='file' and @form='upload_images_form']").send_keys(os.getcwd()+"/redpanda.jpg")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ANALYSE_IMAGES_BUTTON)).click()
        source_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.DRAGGABLE_PANDA))
        dest_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.NON_PANDA_ZONE))
        ActionChains(self.driver).drag_and_drop(source_element, dest_element).perform()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.UPLOAD_IMAGES_BUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.CAMERA_0015_CHECKBOX))
        # time.sleep(3)

    def add_panda_sighting(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.OTHER_CHECKBOX)).click()
        self.driver.find_element_by_xpath("//input[@type='file' and @form='upload_images_form']").send_keys(os.getcwd()+"/redpanda.jpg")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ANALYSE_IMAGES_BUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.UPLOAD_IMAGES_BUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.CAMERA_0015_CHECKBOX))

    def camera_click(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ADD_CAMERA_BUTTON)) #wait for the map to be loaded
        time.sleep(6)
        actions = ActionChains(self.driver)
        actions.move_by_offset(719, 354).click().perform() #camera 0010
        time.sleep(10)
        return "show" in self.driver.find_element_by_id('cameraModal').get_attribute("class")
    
    def panda_sighting_click(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.ADD_CAMERA_BUTTON)) #wait for the map to be loaded
        time.sleep(30)
        actions = ActionChains(self.driver)
        actions.move_by_offset(655, 274).click().perform()
        time.sleep(10)
        return "show" in self.driver.find_element_by_id('pandaModal').get_attribute("class")
        

class MSFTLogin(BasePage):
    def login(self):
        signInWithMSFTbutton = self.driver.find_element_by_tag_name("a")
        signInWithMSFTbutton.send_keys(Keys.RETURN)
        # wait for email field and enter email
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(LoginPageLocators.EMAILFIELD)).send_keys("#enter your msft account email")

        # Click Next
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(LoginPageLocators.NEXTBUTTON)).click()

        # wait for password field and enter password
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(LoginPageLocators.PASSWORDFIELD)).send_keys("#enter your msft account password")

        # Click Login - same id?
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(LoginPageLocators.NEXTBUTTON)).click()