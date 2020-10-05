import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager

class ASVZ_handler(object):

    def __init__(self, login, password, browser='Firefox'):
        # Define a TimeOut limit
        self.delay = 5

        # Store credentials for login
        self.login = login
        self.password = password
        if browser == 'Chrome':
            # Use chrome
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        elif browser == 'Firefox':
            # Set it to Firefox
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    def _login(self):
        # Wait for the event url to load
        try:
            Wait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'eventDetails')))
            print("Event URL loaded successfully!")
        except TimeoutException:
            print("Event URL took too long to load.")

        # Initiate login
        self.driver.find_elements_by_tag_name('button')[1].click()
        
        # Wait for the ASVZ portal to load
        try:
            Wait(self.driver, self.delay).until(EC.presence_of_element_located((By.NAME, 'provider')))
            print("ASVZ portal loaded successfully!")
        except TimeoutException:
            print("ASVZ portal took too long to load.")

        # Go to SWITCHaai portal
        self.driver.find_element_by_name('provider').click()

        # Wait for the SWITCHaai portal to load
        try:
            Wait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'userIdPSelection_iddtext')))
            print("SWITCHaai portal loaded successfully!")
        except TimeoutException:
            print("SWITCHaai portal took too long to load.")

        # Select ETH Zurich
        input_field = self.driver.find_element_by_id("userIdPSelection_iddtext")
        input_field.send_keys('ETH')
        input_field.send_keys(Keys.ENTER)
        
        # Wait for the ETH login page to load
        try:
            Wait(self.driver, self.delay).until(EC.presence_of_element_located((By.NAME, 'j_username')))
            print("ETH login page loaded successfully!")
        except TimeoutException:
            print("ETH login page took too long to load.")

        # Fill in credentials
        login_field = self.driver.find_element_by_name("j_username")
        pass_field = self.driver.find_element_by_name("j_password")

        login_field.send_keys(self.login)
        pass_field.send_keys(self.password)

        # Submit credentials
        self.driver.find_element_by_name('_eventId_proceed').click()

        # Wait for the login process to end
        try:
            Wait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'eventDetails')))
            print("Successfully logged in!")
        except TimeoutException:
            print("Login took too long.")
        

    def enrol(self, url):
        self.driver.get(url)
        # TODO: Log in only 20ish minutes before enrolment
        self._login()
        # TODO: refresh one millisecond after enrolment
        self.driver.refresh()

        # Wait for the refresh to take place
        try:
            Wait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'btnRegister')))
            print("Refresh successful!")
        except TimeoutException:
            print("Refresh took too long.")

        register_button = self.driver.find_element_by_id('btnRegister')
        if register_button.text == "EINSCHREIBUNG FÜR LEKTION ENTFERNEN":
            print("You are already enrolled for this class!")
            return
        register_button.click()

        # Wait for the enrolment to take place
        try:
            Wait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'btnRegister')))
            register_button = self.driver.find_element_by_id('btnRegister')
            if register_button.text == "EINSCHREIBUNG FÜR LEKTION ENTFERNEN":
                print("Enrolment successful! :D")
            else:
                print("Something went wrong and the enrolment wasn't successful :(")
        except TimeoutException:
            print("Enrolment took too long.")

 
if __name__ == '__main__':
    # Enter your login credentials here
    fb_login = ASVZ_handler(login='ccardona', password='HQaF6j3E6mqtrad')
    fb_login.enrol('https://schalter.asvz.ch/tn/lessons/139683')
