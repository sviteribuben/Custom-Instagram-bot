from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
from selenium.common.exceptions import NoSuchElementException
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
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)
        # имитируем скрол страницы
        for i in range(1, 4):  # 4 скрола
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(random.randrange(3, 5))

        # сoбираем все ссылки со страницы
        hrefs = browser.find_elements_by_tag_name('a')
        # формируем список нужных ссылок
        posts_url = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
        # print(posts_url)
        # лайкаем все посты по хэштегу
        for url in posts_url:
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

    # проверяем по xpath существует ли элемент на странице
    def xpath_exist(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # ставим лайк на пост по прямой ссылке

    def put_exactly_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exist(wrong_userpage):
            print('Поста не существует проверь URL')
            self.close_browser()
        else:
            print('Пост успешно найден, ставим лайк')
            time.sleep(2)

            like_button = "html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(2)
            print(f'Лайк на пост {userpost} успешно поставлен')
            self.close_browser()

    def put_many_likes(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exist(wrong_userpage):
            print('Юзера не существует проверь URL')
            self.close_browser()
        else:
            print('Юзер успешно найден, ставим лайк')
            time.sleep(2)

            post_count = int(browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
            loops_count = int(post_count / 12)
            print(loops_count)
            time.sleep(2)

            posts_urls = []
#проверка условия прокрутки страницы если мало простов то else
            if loops_count > 0:
                for i in range(0, loops_count):
                    hrefs = browser.find_elements_by_tag_name('a')
                    hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                    for href in hrefs:
                        posts_urls.append(href)

                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.randrange(3, 5))
                    print(f"Итерация #{i}")
            else:
                print("прокрутка не требуется")
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                for href in hrefs:
                    posts_urls.append(href)
                time.sleep(random.randrange(3, 5))

            file_name = userpage.split('/')[-2]

            with open(f'{file_name}.txt', 'a', encoding='utf-8') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            # избавимся от задвоения сслыок и внесем рандом
            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a', encoding='utf-8') as f:
                for post_url in set_posts_urls:
                    f.write(post_url + '\n')

            # лайкаем
            with open(f'{file_name}_set.txt') as file:
                urls_list = file.readlines()

                for post_url in urls_list[:10]:
                    try:
                        browser.get(post_url)
                        time.sleep(2)

                        like_button = "html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                        browser.find_element_by_xpath(like_button).click()
                        # time.sleep(random.randrange(80, 100))
                        time.sleep(2)

                        print(f'Лайк на пост {post_url} успешно поставлен')
                    except Exception as ex:
                        print(ex)
                        self.close_browser()

            self.close_browser()


my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.put_many_likes('https://www.instagram.com/doctorkolesnik_/')
# my_bot.put_exactly_like('https://www.instagram.com/p/B9j0VnRoDOJ/')
# my_bot.like_photo_by_hastag('data')
