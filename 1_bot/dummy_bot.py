from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
# импортируем модули time and random to create pause
import time
import random


def login(username, password):
    """создаем экземпляр класса гугл хром и передаем ему
    в качестве параметра путь до драйвера"""
    browser = webdriver.Chrome('../chromedriver/chromedriver.exe')
    try:
        browser.get('https://instagram.com')
        #установим рандомную паузу от 3-до 5
        time.sleep(random.randrange(3, 5))
    #находим поле ввода юзернейма
        username_input = browser.find_element_by_name('username')
    #очищаем на всякий случай
        username_input.clear()
    #вводим наш юзернэйм
        username_input.send_keys(username)
        # 2 sec delay
        time.sleep(2)
        # находим поле ввода пароля
        password_input = browser.find_element_by_name('password')
        # очищаем на всякий случай
        password_input.clear()
        # вводим наш пароль
        password_input.send_keys(password)

        #нажимаем на кнопку ввода
        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

        #закрываем вкладку в браузере и выходим
        browser.close()
        browser.quit()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()

login(username, password)

