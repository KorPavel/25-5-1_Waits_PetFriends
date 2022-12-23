from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings import valid_email, valid_password


class TestPetFriends:

    def setup(self):
        self.url = 'https://petfriends.skillfactory.ru/'
        self.name = 'SF_Tester'
        self.login = valid_email
        self.password = valid_password

    def test_all_my_pets_table(self, browser):
        wait_5 = WebDriverWait(browser, 5)  # Устанавливаем явные ожидания 5 сек
        browser.get(self.url)
        assert wait_5.until(EC.presence_of_element_located(
            (By.TAG_NAME, 'h1'))).text == 'PetFriends'
        assert wait_5.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'btn')))
        browser.find_element(By.CLASS_NAME, 'btn').click()
        browser.find_element(By.CSS_SELECTOR, '[href="/login"]').click()
        assert wait_5.until(
            EC.url_to_be('https://petfriends.skillfactory.ru/login'))
        browser.find_element(By.ID, 'email').send_keys(self.login)
        browser.find_element(By.ID, 'pass').send_keys(self.password)
        browser.find_element(By.CLASS_NAME, 'btn').click()
        assert wait_5.until(
            EC.url_to_be('https://petfriends.skillfactory.ru/all_pets'))
        assert wait_5.until(EC.text_to_be_present_in_element(
            (By.TAG_NAME, 'h1'), 'PetFriends'))
        browser.find_element(By.CSS_SELECTOR, '[href="/my_pets"]').click()
        assert wait_5.until(
            EC.url_to_be('https://petfriends.skillfactory.ru/my_pets'))
        assert wait_5.until(EC.presence_of_element_located(
            (By.TAG_NAME, 'h2'))).text == self.name
        pets_info = browser.find_element(By.CLASS_NAME, 'left').text
        # print(repr(pets_info))
        my_pets_amount = int(pets_info.split(': ')[1].split('\n')[0])
        # print(f'\nКоличество моих питомцев: {my_pets_amount}')
        my_pets_tabl = browser.find_elements(By.ID, 'all_my_pets')
        list_my_pets = str(*[elem.text for elem in my_pets_tabl]).split('\n')[1::2]
        # print(list_my_pets)
        pets_image = browser.find_elements(By.TAG_NAME, 'img')
        list_image = [1 * (el.get_attribute('src') != '') for el in pets_image][:-1]
        # print(list_image)
        assert len(list_my_pets) == my_pets_amount, 'Количество питомцев не совпадает с таблицей'
        assert sum(list_image)/len(list_my_pets) > 0.5, 'Фото не имеют больше 50% питомцев'
        assert all([len(elem.split()) == 3 for elem in list_my_pets]), 'Не все питомцы имеют имя, породу и возраст'
        pet_names = [elem.split()[0] for elem in list_my_pets]
        assert len(pet_names) == len(set(pet_names)), 'Имеются повторяющиеся имена'
        assert len(list_my_pets) == len(set(list_my_pets)), 'Имеются повторяющиеся питомцы'
