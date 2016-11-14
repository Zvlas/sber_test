# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pytest
import meth as wp
import allure


def setup_module(module):
    global browser, wait
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")  # игнорим сертификаты безопасности
    options.add_argument("start-maximized")  # браузер фулскрин
    browser = webdriver.Chrome(chrome_options=options)
    wait = WebDriverWait(browser, 20)
    pass


def teardown_module(module):
    browser.close()
    browser.quit()
    pass


@pytest.mark.parametrize('url',[('http://www.sberbank.ru/ru/person')])
@pytest.mark.parametrize('widget_name',[(u'Курсы')])
@pytest.mark.parametrize('redirect_button',[(u'Отделения банка')])
@pytest.mark.parametrize('redirect_url',[('http://www.sberbank.ru/ru/about/today/oib')])
def test_redirect(url,redirect_url,widget_name,redirect_button):
    with allure.step('Загрука вебдрайвера и переход на страницу Сбербанка'):
        wp.open_url(browser, url)
    with allure.step('Ожидание готовности страницы Сбербанка'):
        assert wp.waitForDocumentReady(browser)
    with allure.step('Ожидание загрузки виджета'):
        elemnt_action = wp.ElemntAction(browser)
        elemnt_action.visible("css_selector","div[data-pid='personalRates']")
    with allure.step('Проверка названия виджета'):
        assert browser.find_element_by_css_selector("div[data-pid='personalRates']").text.startswith(widget_name)
    widget_elem = browser.find_element_by_css_selector("div[data-pid='personalRates']")
    with allure.step('Переход из виджета'):
        for elem in widget_elem.find_elements_by_tag_name('p'):
            if elem.text.startswith(redirect_button):
                elem.click()
                break
    with allure.step('Проверка перехода'):
        assert browser.current_url == redirect_url
