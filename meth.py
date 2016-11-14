# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json


def waitForDocumentReady(browser):
    start_time = time.time()
    while time.time() - start_time < 40:
        try:
            browser.execute_script('return document.readyState == "complete"')
        except WebDriverException:
            pass
        else:
            return True
        time.sleep(0.1)
    else:
        return False


def open_url(browser, url):
    browser.get(url)
    browser.maximize_window()


class ElemntAction:
    def __init__(self, _browser):
        self.browser = _browser

    def find_alias(self, type_, name):
        alias = None
        if type_ == "id":
            alias = self.browser.find_element_by_id(name)
        elif type_ == "name":
            alias = self.browser.find_element_by_name(name)
        elif type_ == "xpath":
            alias = self.browser.find_element_by_xpath(name)
        elif type_ == "class_name":
            alias = self.browser.find_element_by_class_name(name)
        elif type_ == "css_selector":
            alias = self.browser.find_element_by_css_selector(name)
        elif type_ == "PARTIAL_LINK_TEXT":
            alias = self.browser.find_element_by_partial_link_text(name)
        else:
            raise ValueError("Can't locate find_metod %s" % type_)
        return alias

    def check_page_element(self, method, type_, name, delay=False):
        wait = WebDriverWait(self.browser, 20)
        find_by_metods = {
            "id": By.ID,
            "name": By.NAME,
            "class_name": By.CLASS_NAME,
            "xpath": By.XPATH,
            "link": By.LINK_TEXT,
            "css_selector": By.CSS_SELECTOR,
            "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
            "TAG_NAME": By.TAG_NAME
        }
        action_metods = {
            "title": EC.title_is,  # An expectation for checking the title of a page.
            "click": EC.element_to_be_clickable,  # checking an element is visible and enabled to click it.
            "present": EC.presence_of_element_located,  # checking that an element is present on the DOM of a page
            "visible": EC.visibility_of_element_located,# checking that an element is present on the DOM of a page and visible
            "frame": EC.frame_to_be_available_and_switch_to_it,# checking whether the given frame is available to switch
            "no_present": EC.invisibility_of_element_located,# checking that an element is either invisible or not present on the DO
            "no_available": EC.staleness_of,  # Wait until an element is no longer attached to the DOM
            "select": EC.element_to_be_selected,  # checking the selection is selected. element is WebElement object
        }
        if not action_metods.get(method):
            print("check_page_element: no instructions for action [%s]" % method)
        try:
            x_wait = wait if not delay else WebDriverWait(self.browser, delay)
            x_wait.until(action_metods[method]((find_by_metods[type_], name)))
            return True
        except:
            print ("Can't find element (%s, %s)" % (type_, name))
            return False

    def click(self, type_, name):
        if self.check_page_element("click", type_, name):
            self.find_alias(type_, name).click()
            time.sleep(0.1)
            return True
        else:
            print ("2 Can't find element (%s, %s)" % (type_, name))
            return False

    def visible(self, type_, name):
        if self.check_page_element("click", type_, name):
            return True
        else:
            print ("Can't find element (%s, %s)" % (type_, name))
            return False

    def no_present(self, type_, name):
        if self.check_page_element("no_present", type_, name):
            return True
        else:
            print ("Can't find element (%s, %s)" % (type_, name))
            return False

    def input(self, type_, name):
        _name = name[0]
        value = name[1]
        if self.check_page_element(self.browser, "click", type_, _name):
            self.find_alias(type_, _name).send_keys(value)
            time.sleep(0.2)
            return True
        else:
            print ("Can't find element (%s, %s)" % (type_, _name))
            return False

    def input_rename(self, type_, name):
        _name = name[0]
        value = name[1]
        if self.check_page_element("click", type_, _name):
            self.find_alias(type_, _name).clear()
            self.find_alias(type_, _name).send_keys(value)
            time.sleep(0.2)
            return True
        else:
            print ("Can't find element (%s, %s)" % (type, _name))
            return False
