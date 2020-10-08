from datetime import datetime, timedelta
import argparse
from apscheduler.schedulers.background import BackgroundScheduler as Scheduler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager

class ASVZ_handler(object):

    def __init__(self, user, password, browser='Firefox', headless=True):
        # Define a TimeOut limit
        self.delay = 5

        # Store credentials for login
        self.user = user
        self.password = password
        if browser == 'Chrome':
            # Use chrome
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('headless')
            self.driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
        elif browser == 'Firefox':
            # Set it to Firefox
            options = Options()
            options.headless = headless
            self.driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())

    def _login(self):
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
        user_field = self.driver.find_element_by_name("j_username")
        pass_field = self.driver.find_element_by_name("j_password")

        user_field.send_keys(self.user)
        pass_field.send_keys(self.password)

        # Submit credentials
        self.driver.find_element_by_name('_eventId_proceed').click()

        # Wait for the login process to end
        try:
            Wait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'eventDetails')))
            print("Successfully logged in!")
        except TimeoutException:
            print("Login took too long.")
        
    def _enrol(self):
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

    def _get_enrolment_time(self):
        for elem in self.driver.find_elements_by_tag_name('dd'):
            if elem.text.count(',') == 2:
                date = elem.text.split('-')[0][4:-1]
        parsed_date = datetime.strptime(date, '%d.%m.%Y %H:%M')
        return parsed_date

    def enrol(self, url):
        # Get the Event URL
        self.driver.get(url)

       # Wait for the event url to load
        try:
            Wait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'eventDetails')))
            print("Event URL loaded successfully!")
        except TimeoutException:
            print("Event URL took too long to load.")

        # Get enrolment time and login time (1 min before enrolment)
        enrolment_time = self._get_enrolment_time() + timedelta(milliseconds=500)
        login_time = enrolment_time - timedelta(minutes=1)

        # Setup the scheduler with both jobs
        scheduler = Scheduler()
        scheduler.add_job(self._login, 'date',run_date=login_time)
        scheduler.add_job(self._enrol, 'date',run_date=enrolment_time)
        scheduler.start()
        
        while scheduler.get_jobs():
            pass
        scheduler.shutdown()
    
 
def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--user', '-u', type=str, required=True,
                        help='Username of your ASVZ account')
    parser.add_argument('--password', '-p', type=str, required=True,
                        help='Password of your ASVZ account')
    parser.add_argument('--url', type=str, required=True,
                        help='URL of the activity to be enroled in')

    args = parser.parse_args()
    return args
 
if __name__ == '__main__':
    # Parse arguments
    args = parse_args()

    # Enter your login credentials here
    asvz = ASVZ_handler(user=args.user, password=args.password)
    asvz.enrol(args.url)
