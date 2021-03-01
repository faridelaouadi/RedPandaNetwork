from selenium.webdriver.common.by import By

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    MAP = (By.ID, 'myMap')
    ADD_CAMERA_BUTTON = (By.XPATH, "//button[@data-target='#editCamerasModal']")
    CAMERA_0010_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and @onclick='filterSymbols(this, '0010')']")
    ADD_CAMERA_BUTTON_WITHIN_MODAL = (By.XPATH, "//input[@form='add_camera_form']")
    ADD_CAMERA_PROPOSED_CAMERA_ID = (By.ID, 'proposedCameraID')
    ADD_CAMERA_LATITUDE = (By.XPATH, "//input[@placeholder='Latitude']")
    ADD_CAMERA_LONGITUDE = (By.XPATH, "//input[@placeholder='Longitude']")
    TOGGLE_MENU = (By.XPATH, "//a[@class='nav-link toggle-menu ']")
    UPLOAD_PAGE_LINK = (By.XPATH, "//a[@href='/upload']")
    CAMERA_0015_CHECKBOX = (By.ID, 'cameraChoice_0015')
    OTHER_CHECKBOX = (By.ID, 'cameraChoice_other')
    ANALYSE_IMAGES_BUTTON = (By.XPATH, "//input[@type='submit' and @form='upload_images_form']")
    UPLOAD_IMAGES_BUTTON = (By.ID, 'upload_images')
    DRAGGABLE_PANDA = (By.XPATH, "//li[@class='ui-widget-content ui-corner-tr ui-draggable ui-draggable-handle']")
    NON_PANDA_ZONE = (By.ID, 'non_panda_zone')


class LoginPageLocators(object):
    EMAILFIELD = (By.ID, "i0116")
    PASSWORDFIELD = (By.ID, "i0118")
    NEXTBUTTON = (By.ID, "idSIButton9")
