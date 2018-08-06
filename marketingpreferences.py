from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import re


def is_valid_email(email):
    if len(email) > 7:
        if re.match(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+', email):
            return True

    return False


def set_preferences(email_address):
    driver = webdriver.Firefox()
    wait = ui.WebDriverWait(driver, 10)
    driver.maximize_window()
    driver.switch_to.window(driver.current_window_handle)
    driver.get('https://pages.awscloud.com/communication-preferences.html')

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

    # submit the form
    submit = driver.find_element(By.XPATH, '//*[@id="BtnLabel"]')
    submit.click()

    # wait for the page to load
    wait.until(lambda d: d.title == 'Unsubscribe Success')

    driver.quit()


text_file = open("email_list.txt", "r")
emails = text_file.readlines()

for email in emails:
    email = email.rstrip("\n\r")
    if is_valid_email(email):
        set_preferences(email)
