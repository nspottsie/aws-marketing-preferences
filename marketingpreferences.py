from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import re
import argparse
import time


def parse_emails():
    parser = argparse.ArgumentParser(description='Process the list of space separated email addresses passed from the command line.')

    parser.add_argument('-e', '--emails', metavar='E', nargs='+', default=[],
                        help='A space separated list of emails addresses')

    args = parser.parse_args()

    return args.emails


def is_valid_email(email):
    if len(email) > 7:
        if re.match(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+', email):
            return True

    return False


def set_preferences(email_address):
    try_count = 0
    driver = None

    while try_count < 10:
        try_count += 1
        try:
            driver = webdriver.Remote(
                command_executor='http://firefox-standalone:4444/wd/hub',
                desired_capabilities={'browserName': 'firefox', 'javascriptEnabled': True}
            )
            break
        except:
            print("Unable to connect to Selenium, waiting 10s to try again")
            time.sleep(10)

    if driver is None:
        raise Exception("Unable to connect to Selenium after 10 attempts. Exiting")

    try:
        wait = ui.WebDriverWait(driver, 10)
        driver.maximize_window()
        driver.switch_to.window(driver.current_window_handle)
        driver.get('https://pages.awscloud.com/communication-preferences.html')
        driver.save_screenshot('screen_shot_1.png')

        # input the email address to unsubscribe
        email = driver.find_elements(By.XPATH, '//*[@id="Email"]')[0]
        email.send_keys(email_address)

        # set language to english
        language = driver.find_elements(By.XPATH, '//*[@id="PreferenceCenter_Language_Preference__c"]')[0]
        for option in language.find_elements_by_tag_name('option'):
            if option.text == 'English':
                option.click()
                break

        # tick the checkbox for unsubscribing from all emails
        checkbox = driver.find_elements(By.XPATH, '//input[@name="Unsubscribed"]')[0]
        checkbox.click()

        driver.save_screenshot('screen_shot_2.png')

        # submit the form
        submit = driver.find_element(By.XPATH, '//*[@id="BtnLabel"]')
        submit.click()

        # wait for the page to load
        wait.until(lambda d: d.title == 'Unsubscribe Success')
    finally:
        driver.quit()


print("Marketing preferences container starting up")
emails = parse_emails()
print("List of emails to process:", emails)

for email in emails:
    if is_valid_email(email):
        print("Setting preferences for valid email address:", email)
        set_preferences(email)
    else:
        print("Skipping invalid email:", email)
