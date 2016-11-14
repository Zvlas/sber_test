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
#

def teardown_module(module):
    browser.close()
    browser.quit()
    pass




@pytest.mark.parametrize('url',[('http://www.sberbank.ru/ru/person')])
@pytest.mark.parametrize('widget_name',[(u'Курсы')])
def test_redirect(url,widget_name):
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
    widget_elemnt_action = wp.ElemntAction(widget_elem)
    with allure.step('Активация настроек виджета'):
        assert widget_elemnt_action.click('class_name','hide-i')

    with allure.step('Проверка видимости кнопки удаления'):
        assert widget_elemnt_action.visible('class_name','remove-w')

    with allure.step('Удаление виджета'):
        assert widget_elemnt_action.click('class_name','remove-w')
        # assert widget_elemnt_action.click('class_name','remove-w') # Если это раскоментировать то тест будет пройден, у cбербанка баг=))

    with allure.step('Проверка факта удаления'):
        assert widget_elemnt_action.no_present('class_name','hide-i')

