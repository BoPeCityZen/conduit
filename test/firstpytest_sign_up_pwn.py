## 1. Sign up automatizálása

import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestSingUp(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-position=-1000,0')
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "http://localhost:1667/"
        self.browser.get(URL)
        self.browser.maximize_window()

        # WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]')))
        # sign_up_mnu_btn = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        # sign_up_mnu_btn.click()

    def teardown_mwthod(self):
        self.browser.quit()

    @allure.id('TC1 P+')
    @allure.title('Regisztráció - Míg sikeres nem lesz')
    def test_sign_up_negativ_and_pozitiv(self, Username_n = ['user1'], Email_n = ['user1@hotmail.com'], Password = 'Userpass1', reg_succ = ''):

        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]')))
        sign_up_mnu_btn = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        sign_up_mnu_btn.click()

        ### Inputmezők kigyűjtése
        input_Username = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        input_Email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        input_password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')

        n = 1
        ### Regisztrációs kisérlet-lánc default adatokkal, míg sikeres nem lesz
        while reg_succ != 'Welcome!':
            ### inputmezők kitöltése
            input_Username.send_keys(Username_n[-1])
            input_Email.send_keys(Email_n[-1])
            input_password.send_keys(Password)

            sign_up_btn = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
            assert sign_up_btn.is_displayed()
            sign_up_btn.click()

            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
            reg_succ = self.browser.find_element(By.XPATH, '//div[@class="swal-title"]').text
            reg_succ_s = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]').text

            if reg_succ == 'Registration failed!':
                ### REG. ELLENŐRZÉSE INDIREKT NEGATÍV ÁGON - SIKERTELEN REG.
                assert reg_succ == 'Registration failed!'
                assert reg_succ_s == 'Email already taken.'
                reg_succ_N = reg_succ
                reg_succ_s_N = reg_succ_s

                ### Új belépési adatokat generálása n érték növelésével mivel az adott 'usern' név már foglalt volt
                n += 1
                Username_n.append(f'user{str(n)}')
                Email_n.append(f'user{str(n)}@hotmail.com')

                ok_btn = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]')))
                ok_btn.click()

            else:
                if n == 1:
                    reg_succ_N = 'Sikeres regisztráció'
                    reg_succ_s_N = 'elsőre'

                ### REG. ELLENŐRZÉSE POZITÍV ÁGON - SIKERES REG.
                assert reg_succ == 'Welcome!'
                assert reg_succ_s == 'Your registration was successful!'
                if reg_succ == 'Welcome!':
                    print(f'\n{n - 1} negatív ágon lefuttatott Assert: {reg_succ_N} ({reg_succ_s_N}) után: ')
                    print(f"Assert a pozitív ágon: {reg_succ} ({reg_succ_s})")

        # böngésző bezárása
        self.browser.quit()

    @allure.id('TC1 N-')
    @allure.title('Regisztrációs kisérlet - jelszó nélkül')
    def test_sign_up_direct_negativ(self, Username_nope = 'user', Email_nope = 'user@hotmail.com', Password_nope = ''):
        ### belépési kisérlet jelszó nélkül - direkt negatív ág

        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]')))
        sign_up_mnu_btn = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        sign_up_mnu_btn.click()

        ### Inputmezők kigyűjtése
        input_Username = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        input_Email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        input_password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')

        ### inputmezők kitöltése
        input_Username.send_keys(Username_nope)
        input_Email.send_keys(Email_nope)
        input_password.send_keys(Password_nope)

        sign_up_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
        assert sign_up_btn.is_displayed()
        sign_up_btn.click()

        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
        reg_succ = self.browser.find_element(By.XPATH, '//div[@class="swal-title"]').text
        reg_succ_s = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]').text

        if reg_succ == 'Registration failed!':
            ### REG. ELLENŐRZÉSE DIREKT NEGATÍV ÁGON - SIKERTELEN REG.
            assert reg_succ == 'Registration failed!'
            assert reg_succ_s == 'Password field required.'
            print(f'\nAssert direkt negatív ágon: {reg_succ} ({reg_succ_s})')
            ok_btn = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]')))
            ok_btn.click()

        # böngésző bezárása
        self.browser.quit()
