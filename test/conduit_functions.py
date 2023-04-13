import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from conduit_test_data import useData


class callFunctions(useData):

    def useRegistrationButton(self):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]'))).click()

    def useSignInButton(self):
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]'))).click()

    def log_in_btn(self):
        login_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))
        return login_btn

    def log_out_btn(self):
        logou_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//i[@class="ion-android-exit"]')))
        return logou_btn

    def gathering_input_fields(self, inp_fields_elements: dict, placeholders_dict: dict):
        placeholders = list(placeholders_dict.keys())
        # placeholders = ["Username", "Email", "Password"] # a kód kezdeti fázisban előre def. értékekkel ment
        # print(placeholders)
        for field in range(len(placeholders)):
            inp_fields_elements[f'{placeholders[field]}'] = self.browser.find_element(By.XPATH,
                                                                                      f'//input[@placeholder="{placeholders[field]}"]')
        return inp_fields_elements

    def send_inputs(self, inpFields_dict, inp_dict_sub):
        # inputmezők kitöltése és küldése fgv-ből nyert dict-ek kulcs/érték átadásával
        for pairs in inpFields_dict.items():
            inpName = pairs[0]
            inpValue = pairs[1]
            # print(f'key&value: {inpName}={inpValue}') # ellenőrző sor
            send_this_key = inp_dict_sub[inpName]
            inpValue.send_keys(send_this_key)

        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]'))).click()

    def reg_process_init(self, keyword: str):
        ### reg. folyamat indítása menűpont kattintásával
        self.useRegistrationButton()

        ### Input értékek kigyűjtése, mezők kitöltése és elküldése
        inp_dict_sub = self.inp_values(sub_dict=keyword)
        inpFields_dict = self.gathering_input_fields(inp_fields_elements={}, placeholders_dict=inp_dict_sub)
        self.send_inputs(inpFields_dict, inp_dict_sub)

    def popup_text(self, actual_str: dict):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
        actual_str['swal_title'] = self.browser.find_element(By.XPATH, '//div[@class="swal-title"]').text
        actual_str['swal_text'] = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]').text
        return actual_str

    def click_popup_ok_btn(self):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]'))).click()

    def locate_navbar_items(self):
        navbar_items = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')))
        return navbar_items

    def signin_rutin(self):
        self.useSignInButton()
        inp_dict_sub = self.inp_values(sub_dict='Pass')
        username = inp_dict_sub['Username']
        # print(username)
        del inp_dict_sub['Username']
        # print(inp_dict_sub)
        inpFields_dict = self.gathering_input_fields(inp_fields_elements={}, placeholders_dict=inp_dict_sub)
        self.send_inputs(inpFields_dict, inp_dict_sub)
        return username

    def accept_cookies(self):
        ### sütihasználati politikát elfogadó gomb
        accept_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]/div')))
        return accept_btn

    def tag_list(self):
        actual_tag = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="sidebar"]//div[@class="tag-list"]//a[@class="tag-pill tag-default"]')))
        return actual_tag

    def assert_tag_list(self):
        # Tag lista elemeinek ellenőrzése: honlapon talált Tagek összevetése előre def. Tagekkel
        predef_tags = self.def_tag_list()
        actual_tags = self.tag_list()
        listahossz = len(predef_tags)
        assert len(actual_tags) >= listahossz
        ottvan = 0
        for t in range(len(actual_tags)):
            Nope = True
            tag_name = actual_tags[t].text
            for v in range(listahossz):
                if tag_name == predef_tags[v]:
                    assert tag_name == predef_tags[v]
                    ### Ha egy elemet megtalált, akkor nőveljük az értéket
                    ottvan += 1
                    Nope = False
                    # print(tag_name + " " + str(v) + ". indexel szerpel a Tagek között")
            if Nope:
                pass
                # print(tag_name + " nem szerepel a Tagek között")
        return ottvan, listahossz

    def listed_pages_nav_item(self):
        page_list = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//ul[@class="pagination"]//a[@class="page-link"]')))
        nr_of_pages = len(page_list)
        ### végigjárjuk a több oldalas listát, minden lépésnél lekérve az aktuális oldal számát
        for page in range(nr_of_pages):
            page_list[page].click()
            srn_of_a_page = self.active_page_in_list()
            print(f'{srn_of_a_page} / {nr_of_pages}')
            ### ha végigértünk visszaküldjük az odlaszámokat assertálásra
            if srn_of_a_page == nr_of_pages:
                page_nrs = {'all': nr_of_pages, 'actual': srn_of_a_page}
                return page_nrs

    def active_page_in_list(self):
        active_page = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//ul[@class="pagination"]//li[@class="page-item active"]//a[@class="page-link"]')))
        srn_of_a_p = int(active_page.text)
        return srn_of_a_p

    def use_new_article_btn(self):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]'))).click()

    def use_settings_btn(self):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/settings"]'))).click()

    def sajat_cikkek(self):
        user_nav_btn = self.locate_navbar_items()[3]
        user_nav_btn.click()

        time.sleep(2)
        articles = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="article-preview"]//h1')))
        return articles

    def use_delete_article_btn(self):
        delete_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-outline-danger btn-sm"]')))
        delete_btn.click()

    def create_new_article(self, new_article: dict):
        inp_values = list(new_article.values())
        placeholders = list(new_article.keys())
        text_area = placeholders[2]
        GivenArTitle = new_article['Article Title']

        for field in range(len(placeholders)):
            if placeholders[field] == text_area:
                inp_field = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//textarea[@placeholder="{placeholders[field]}"]')))
            else:
                inp_field = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//input[@placeholder="{placeholders[field]}"]')))
            inp_field.send_keys(inp_values[field])

        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()
        return GivenArTitle

    def Article_title_field(self):
        ArTitleElement = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="container"]//h1')))
        return ArTitleElement

    def change_username(self, name: str):
        your_username_field = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Your username"]')))
        your_username_field.clear()

        your_username_field.send_keys(name)
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]'))).click()
        act_msg = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]'))).text
        return act_msg
