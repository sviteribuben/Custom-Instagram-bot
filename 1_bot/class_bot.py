from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
# импортируем модули time and random to create pause
import time
import random


class InstagramBot():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('../chromedriver/chromedriver.exe')

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        """создаем экземпляр класса гугл хром и передаем ему
           в качестве параметра путь до драйвера"""
        browser = self.browser
        browser.get('https://instagram.com')
        # установим рандомную паузу от 3-до 5
        time.sleep(random.randrange(3, 5))
        # находим поле ввода юзернейма
        username_input = browser.find_element_by_name('username')
        # очищаем на всякий случай
        username_input.clear()
        # вводим наш юзернэйм
        username_input.send_keys(username)
        # 2 sec delay
        time.sleep(2)
        # находим поле ввода пароля
        password_input = browser.find_element_by_name('password')
        # очищаем на всякий случай
        password_input.clear()
        # вводим наш пароль
        password_input.send_keys(password)
        # нажимаем на кнопку ввода
        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    def like_photo_by_hastag(self, hashtag):
        browser = self.browser
        try:
            browser.get('https://instagram.com')
            # установим рандомную паузу от 3-до 5
            time.sleep(random.randrange(3, 5))
            # находим поле ввода юзернейма
            username_input = browser.find_element_by_name('username')
            # очищаем на всякий случай
            username_input.clear()
            # вводим наш юзернэйм
            username_input.send_keys(username)
            # 2 sec delay
            time.sleep(2)
            # находим поле ввода пароля
            password_input = browser.find_element_by_name('password')
            # очищаем на всякий случай
            password_input.clear()
            # вводим наш пароль
            password_input.send_keys(password)

            # нажимаем на кнопку ввода
            password_input.send_keys(Keys.ENTER)
            time.sleep(5)

            # поиск по хэштэгу
            try:
                browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
                time.sleep(5)
                # имитируем скрол страницы
                for i in range(1, 4):  # 4 скрола
                    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(random.randrange(3, 5))

                # сoбираем все ссылки со страницы
                hrefs = browser.find_elements_by_tag_name('a')
                # формируем список нужных ссылок
                posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]


                # лайкаем все посты по хэштегу
                for url in posts_urls:
                    try:
                        browser.get(url)
                        time.sleep(5)
                        # в модальном окне отрабатывать это икспас не будет
                        like_button = browser.find_element_by_xpath(
                            '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                        time.sleep(random.randrange(80, 100))
                    except Exception as ex:
                        print(ex)
                        self.browser.close()




