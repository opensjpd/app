import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestBasic():
  def setup_method(self, method):
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    self.driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub', options=options)
    self.driver.implicitly_wait(10)
    self.driver.get("http://app:8502/")
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()

  def check_exceptions(self):
    exceptions = self.driver.find_elements(By.CLASS_NAME, 'stException')
    assert len(exceptions) == 0, "Found exception: {}".format(exceptions[0].text)

  # Go to a page and check basic things (title, exceptions)
  def go_to_page(self, name):
    self.driver.find_element(By.PARTIAL_LINK_TEXT, name).click()
    time.sleep(5)
    assert self.driver.title == f"{name} - Open SJPD"
    self.check_exceptions()
  
  def test_home(self):
    assert self.driver.title == "Open SJPD"
    # TODO expand

  def test_officer_lookup(self):
    officers = {
      'monzon': {
        'h1': 'Officer Monzon (#4147)',
        'arrests': '101',
        'beats': '40',
        'booking': '94%',
        'age': '26',
        'img': 3,
      },
      'bick': {
        'h1': 'Officer Bick (#077P)',
        'arrests': '76',
        'beats': '10',
        'booking': '5%',
        'age': '44',
        'img': 3,
      },
      'yee': {
        'h1': 'Officer Yee (#4342)',
        'arrests': '507',
        'beats': '40',
        'booking': '26%',
        'age': '37',
        'img': 1,
      }
    }

    self.go_to_page("Officer Lookup")

    for name, data in officers.items():
      self.driver.find_element(By.TAG_NAME, "input").click()
      self.driver.find_element(By.TAG_NAME, "input").send_keys(name)
      self.driver.find_element(By.TAG_NAME, "input").send_keys(Keys.RETURN)
      time.sleep(5)
      self.check_exceptions()

      assert self.driver.find_element(By.TAG_NAME, "h1").text == data['h1']
      
      metrics = self.driver.find_elements(By.XPATH, '//div[@data-testid="stMetricValue"]')
      assert metrics[0].text == data['arrests'], f"Wrong number of arrests for {name}"
      assert metrics[1].text == data['beats']
      assert metrics[2].text == data['booking']
      assert metrics[3].text == data['age']

      assert len(self.driver.find_elements(By.TAG_NAME, "img")) == data['img'], f"Wrong number of graphs for {name}"

  def test_unknown_officer(self):
    self.go_to_page("Officer Lookup")

    officer_select = self.driver.find_element(By.TAG_NAME, "input")
    officer_select.click()
    officer_select.send_keys('UNKNOWN')
    officer_select.send_keys(Keys.RETURN)

    time.sleep(2)
    badge_select = self.driver.find_elements(By.TAG_NAME, "input")[1]
    badge_select.click()
    badge_select.send_keys('28')
    badge_select.send_keys(Keys.DOWN)
    badge_select.send_keys(Keys.RETURN)

    header = self.driver.find_element(By.TAG_NAME, "h1")
    assert header.text == 'Officer Unknown (#2864)'

  def test_unusual_officers(self):
    self.go_to_page("Unusual Officers")

  def test_beat_map(self):
    self.go_to_page("Beat Map")

    race_select = self.driver.find_element(By.TAG_NAME, "input")
    race_select.click()
    race_select.send_keys('CAUCASIAN')
    race_select.send_keys(Keys.RETURN)

    time.sleep(2)
    self.check_exceptions()