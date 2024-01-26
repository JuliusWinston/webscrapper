from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import subprocess
import time

options = webdriver.ChromeOptions()

print("Please enter email: ")
email = input()
print("Please enter password: ")
password = input()
print("Please enter directory where you wish to save downloaded files: ")
download_directory = input()

options.add_experimental_option('prefs', {
  "download.default_directory": download_directory,
  "download.prompt_for_download": False,
  "plugins.always_open_pdf_externally": True
})

try:
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
except Exception as e:
  print(f"Error initializing ChromeDriver: {e}")

def handleAdsModal (): 
  try:
    dismiss_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'dismiss-button')))
    dismiss_button.click()
  except TimeoutException:
    print('No popup modal found')

def handleLoginModal (): 
  try:
    login_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located(login_button_locator))
    driver.execute_script("arguments[0].click();", login_button)

    email_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(email_input_locator))
    email_input.send_keys(email)
    email_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(password_input_locator))
    email_input.send_keys(password)

    login_form = WebDriverWait(driver, 5).until(EC.presence_of_element_located(login_form_locator))
    login_form.submit()

  except TimeoutException:
    print('already logged in...')
    print('if script is not working as intended, please check your internet and restart script')

def install_dependencies():
  subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

install_dependencies()

while True:
  try:
    print('Please enter book title or ctrl C to quit: ')
    book_title = input()
    
    URL = "https://z-library.se"
    driver.get(URL)

    driver.maximize_window()

    input_locator = (By.ID, 'searchFieldx')
    form_locator = (By.ID, 'searchForm')
    search_results = (By.ID, 'searchResultBox')
    login_button_locator = (By.CSS_SELECTOR, '.bookLoginBlock__buttons button[data-action="login"]')
    email_input_locator = (By.NAME, 'email')
    password_input_locator = (By.NAME, 'password')
    signin_button_locator = (By.XPATH, '//button[@type="submit" and @name="submit" and @value="true" and contains(@class, "btn-info")]')
    login_form_locator = (By.ID, 'loginForm')
    download_link_locator = (By.CLASS_NAME, 'addDownloadedBook')

    try:
      input_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located(input_locator))
      search_form = WebDriverWait(driver, 3).until(EC.presence_of_element_located(form_locator))

      if not input_element.get_attribute("value"):
        input_element.send_keys(book_title)
        search_form.submit()

      handleAdsModal()
      
      search_results_boxes = WebDriverWait(driver, 3).until(EC.presence_of_element_located(search_results))

      first_div = search_results_boxes.find_elements(By.CLASS_NAME, 'resItemBox')[0]
      first_a_element = first_div.find_element(By.TAG_NAME, 'a')
      first_a_element.click()

      

      handleLoginModal()
      download_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(download_link_locator))
      download_link.click()

      print('downloading ...')
      time.sleep(2)

    except StaleElementReferenceException:
      print('An error occured, please restart the application')
      break

  except KeyboardInterrupt:
    print('\nScript stopped!')
    break
