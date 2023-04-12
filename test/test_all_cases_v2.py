import csv
import time
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Test11ConduitFunction(object):

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

    def inp_values(self, sub_dict: str):
        inp_dict = {"Pass": {'Username': 'user1',
                             'Email': 'user1@hotmail.com',
                             'Password': 'Userpass1', },
                    "Fail": {'Username': 'user1',
                             'Email': 'user1@hotmail.com',
                             'Password': '', },
                    "While": {'Username': 'user1',
                              'Email': 'user1@hotmail.com',
                              'Password': 'Userpass1', }
                    }
        return inp_dict[sub_dict]



    def send_inputs(self, inpFields_dict, inp_dict_sub):
        # inputmezők kitöltése és küldése fgv-ből nyert dict-ek kulcs/érték átadásával
        for pairs in inpFields_dict.items():
            inpName = pairs[0]
            inpValue = pairs[1]
            # print(f'key&value: {inpName}={inpValue}') # ellenőrző sor
            send_this_key = inp_dict_sub[inpName]
            inpValue.send_keys(send_this_key)

        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]'))).click()

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

    def expected_text(self, info: str):
        expected_str = {"Pass": {'Title': 'Welcome!',
                                 'Text': 'Your registration was successful!'},
                        "Fail": {'Title': 'Registration failed!',
                                 'Text': 'Password field required.'},
                        "While": {'Title': 'Registration failed!',
                                  'Text': 'Email already taken.'},
                        "Accept": {'Text': 'I accept!'},
                        "Update": {'Title': 'Update successful!'},
                        }
        return expected_str[info]

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
        username=inp_dict_sub['Username']
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

    def def_tag_list(self):
        predef_tags = (
        'lorem', 'ipsum', 'dolor', 'nisil', 'urna', 'nunc', 'laoreet', 'dorum', 'loret', 'nibih', 'mitast', 'leo')
        return predef_tags

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


    def use_thisuser_btn(self):
        username=self.inp_values('Pass')['Username']
        # print(username)
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, f'//a[@href="#/@{username}/"]')))[0].click()


    def sajat_cikkek(self):
        self.use_thisuser_btn()
        time.sleep(2)
        articles = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="article-preview"]//h1')))
        return articles

    def use_delete_article_btn(self):
        delete_btn=WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-outline-danger btn-sm"]')))
        delete_btn.click()


    def new_article_dict (self):
        ### key=input placeholder; value=új cikk szövegelemei
        new_article = {"Article Title": "Create UmbEco-style text",
                        "What's this article about?": "How to generate text in Umberto Eco's style ",
                        "Write your article (in markdown)": "Now that the text-writing generated by AI is strengthened, it would be interesting to try to write a book in Umberto Eco's style,  with the help of an chat-AI",
                        "Enter tags": "Umberto, Eco, chat-AI",
                        }
        return new_article

    def create_new_article(self,new_article:dict):
        inp_values = list(new_article.values())
        placeholders = list(new_article.keys())
        text_area = placeholders[2]
        GivenArTitle=new_article['Article Title']

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
        ArTitleElement=WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="container"]//h1')))
        return ArTitleElement

    def change_username(self, name:str):
        your_username_field = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Your username"]')))
        your_username_field.clear()

        your_username_field.send_keys(name)
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]'))).click()
        act_msg = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]'))).text
        return act_msg



    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-position=-1000,0')
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "http://localhost:1667/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        pass
        # self.browser.quit()

    # TC1: Regisztráció----------------------------------------------------------------------------------------------------------------------
    @allure.id('TC1.1. N+')
    @allure.title('Sikertelen regisztrációs kisérlet - jelszó nélkül')
    def test_sign_up_direct_neg(self):
        self.reg_process_init(keyword='Fail')

        ### Asserthez szükséges elvárt és tényleges értékek meghívása funkciókból
        actual_str = self.popup_text(actual_str={})
        expected_str = self.expected_text(info='Fail')

        ## REG. ELLENŐRZÉSE NEGATÍV ÁGON - SIKERES SIKERTELEN REG. :))
        assert actual_str['swal_title'] == expected_str['Title']
        assert actual_str['swal_text'] == expected_str['Text']
        print(f"Assert a negatív ágon: {actual_str['swal_title']} ({actual_str['swal_text']})")

    @allure.id('TC1.2 P+')
    @allure.title('Regisztráció - fix (még nem regisztrált) adatokkal')
    def test_sign_up_fix_poz(self):
        self.reg_process_init(keyword='Pass')

        ### Asserthez szükséges elvárt és tényleges értékek
        actual_str = self.popup_text(actual_str={})
        expected_str = self.expected_text(info='Pass')

        ## REG. ELLENŐRZÉSE POZITÍV ÁGON - SIKERES REG.
        assert actual_str['swal_title'] == expected_str['Title']
        assert actual_str['swal_text'] == expected_str['Text']
        print(f"Assert a pozitív ágon: {actual_str['swal_title']} ({actual_str['swal_text']})")

    # TC1: Regisztáció -----------------------------------------------------------------------------------------------------------------------
    @allure.id('TC1.3 cond P+ ')
    @allure.title('Regisztráció - Míg sikeres nem lesz (ha a próbált felhasználónév már foglalt lenne)')
    def test_sign_up_while(self):
        ### reg. folyamat indítása menűpont kattintásával
        self.useRegistrationButton()

        ### Inputmezők adatainak kigyűjtése - küldés a while cikluson belül
        inp_dict_sub = self.inp_values(sub_dict='While')
        inpFields_dict = self.gathering_input_fields(inp_fields_elements={}, placeholders_dict=inp_dict_sub)

        ### Asserthez szükséges elvárt és tényleges értékek
        expected_Pstr = self.expected_text(info='Pass')
        popup_title = ''

        n = 1
        while popup_title != expected_Pstr['Title']:

            self.send_inputs(inpFields_dict, inp_dict_sub)

            actual_str = self.popup_text(actual_str={})
            expected_Fstr = self.expected_text(info='While')
            popup_title = actual_str['swal_title']

            if actual_str['swal_title'] == expected_Fstr['Title']:
                ### REG. ELLENŐRZÉSE INDIREKT NEGATÍV ÁGON - SIKERTELEN REG.
                assert actual_str['swal_title'] == expected_Fstr['Title']
                assert actual_str['swal_text'] == expected_Fstr['Text']
                ### Alábbi csak a konzolos 'többletinfó' kiíratáshoz szükséges
                reg_succ_N = expected_Fstr['Title']
                reg_succ_s_N = expected_Fstr['Text']

                ### Új belépési adatokat generálása n érték növelésével mivel az adott 'user#n' név már foglalt volt
                n += 1
                inp_dict_sub.update({'Username': f'user{n}',
                                     'Email': f'user{n}@hotmail.com', })

                self.click_popup_ok_btn()

            else:
                if n == 1:
                    ### Alábbi csak a konzolos 'többletinfó' kiíratáshoz szükséges
                    reg_succ_N = 'Sikeres regisztráció'
                    reg_succ_s_N = 'elsőre'

                ### REG. ELLENŐRZÉSE POZITÍV ÁGON - SIKERES REG.
                assert actual_str['swal_title'] == expected_Pstr['Title']
                assert actual_str['swal_text'] == expected_Pstr['Text']
                if actual_str['swal_title'] == expected_Pstr['Title']:
                    ### Alábbi csak a konzolos 'többletinfó' kiíratáshoz szükséges
                    print(f'\n{n - 1} negatív ágon lefuttatott Assert: {reg_succ_N} ({reg_succ_s_N}) után: ')
                    print(f"Assert a pozitív ágon: {actual_str['swal_title']} ({actual_str['swal_text']})")

    # TC2: Bejelentkezés --------------------------------------------------------------------------------------------------------------------
    @allure.id('TC2. P+')
    @allure.title('Belépés sikerességének ellenőrzése navbar menu elemszámával, a "Log out" gomb meglétével')
    def test_sign_in(self):
        self.signin_rutin()

        time.sleep(2)
        self.browser.refresh()
        navbar_items = self.locate_navbar_items()
        menusor_hossz = len(navbar_items)
        if menusor_hossz == 5:  # sikeres belépés
            ### Pozitív ág belépésre: belépést követően a fejlécmenű elemei 5-re változnak
            assert menusor_hossz == 5
            print(f'\nMenuelemek száma {menusor_hossz} -> Belépés megvalósult!')

            ### assert "Log out" gomb meglétének ellenőrzésével
            logout_btn = self.log_out_btn()
            assert logout_btn
            print(f'Igazolt belépés: A kilépés gomb lokalizálható!')

            ### assert "Log out" felírat meglétének ellenőrzésével
            log_out_btn_txt = navbar_items[-1].text
            assert log_out_btn_txt == ' Log out'
            print(f'Igazolt belépés: "{log_out_btn_txt}" szöveg megjelent!')

    # TC3: Adatkezelési nyilatkozat használata ----------------------------------------------------------------------------------------------
    @allure.id('TC3. P+')
    @allure.title('Cookie policy - "I accept!" gombfelírat ellenőrzése')
    def test_gdpr_acceptance(self):
        self.signin_rutin()

        ### sütihasználati politikát elfogadó gomb
        accept_btn = self.accept_cookies()

        ### Öszzevetésre szánt gombfelíratok lekérése
        accept_btn_text = accept_btn.text
        expected_str = self.expected_text(info='Accept')
        ## cookie policy elfogadásához tartotzó gomb szövegének ellenőrzése - 'I accept!' gomb
        assert accept_btn_text == expected_str['Text']

        # accept_btn.click()

    # TC4:	Adatok listázása-----------------------------------------------------------------------------------------------------------------
    @allure.id('TC4. P+')
    @allure.title('Adatok listázásának ellenőrzése')
    def test_listed_data(self):
        self.signin_rutin()

        # Tag list elemeinek ellenőrzése kiszervezett funkc-val
        ott_van = self.assert_tag_list()

        # Az ellenőrzés lényege, hogy az összes előre definiált Tag elemet megtalálta-e
        assert ott_van[0] == ott_van[1]

    # TC5: Több oldalas lista bejárása-------------------------------------------------------------------------------------------------------
    @allure.id('TC5. N+')
    @allure.title('Több oldalas lista bejárása')
    def test_going_trough_multi_page_list(self):
        self.signin_rutin()

        ### alábbi funkcióval végigjárjuk a több oldalas listát, minden lépésnél lekérve az aktuális oldal számát
        nrs_of_listed_pages = self.listed_pages_nav_item()

        assert nrs_of_listed_pages['all'] == nrs_of_listed_pages['actual']


    # TC6: Új adat bevitel-------------------------------------------------------------------------------------------------------------------
    @allure.id('TC6. P+')
    @allure.title('Új adat bevitel')
    def test_put_new_article(self):
        self.signin_rutin()

        ### cikkszerkesztő felület nyitása a weblapon
        self.use_new_article_btn()

        ### cikkadatok bekérése funkció hívással
        new_article = self.new_article_dict()

        ### Az új cikk felvétele a bekért cikkadatokból az editor inputmezőibe kiszervezett funkcióval
        GiveNewArTitle=self.create_new_article(new_article)

        DispArTitle=self.Article_title_field().text
        ### Ellenőrizzük a megjelenő cikk címezejét, hogy egyezik-e a beküldött címadattal
        assert DispArTitle == GiveNewArTitle


    # TC7: Ismételt és sorozatos adatbevitel adatforrásból-----------------------------------------------------------------------------------
    @allure.id('TC7. P+')
    @allure.title('Sorozatos adatbevitel csv fájlból')
    def test_more_article_from_external_source(self):
        self.signin_rutin()

        with open('test/articles_to_publish.csv', 'r', encoding='UTF-8') as file:
            articles_table = csv.reader(file, delimiter=';')
            ### A csv file első sora az inputmezőket azonosító placeholder
            csv_headings = next(articles_table)

            new_article = dict()
            for row in articles_table:
                for element in range(len(csv_headings)):
                    ### A csv fileból soronként kreálunk egy dictionaryt a sorozatos adatmegadáshoz
                    new_article[csv_headings[element]] = row[element]

                ### cikkszerkesztő felület nyitása a weblapon
                self.use_new_article_btn()
                ### Az új cikk felvétele a bekért cikkadatokból az editor inputmezőibe kiszervezett funkcióval
                GiveNewArTitle = self.create_new_article(new_article)

                DispArTitle=self.Article_title_field().text
                ### Ellenőrizzük a megjelenő cikk címezejét, hogy egyezik-e a beküldött címadattal
                print(f'Bevitt cím-->> {GiveNewArTitle} <Vs> {DispArTitle} <<--megjelenő cím')
                assert DispArTitle == GiveNewArTitle



    # TC8: Meglévő adat módosítás------------------------------------------------------------------------------------------------------------
    @allure.id('TC8. P+')
    @allure.title('Meglévő adat módosítás')
    def test_update_data(self):
        username=self.signin_rutin()
        newname=f'BrandNew{username}'
        self.use_settings_btn()
        ### elvégezzük a névváltoztatást és ellenőrizzük a visszaigazoló üzenetet kiszervezett funkcióban
        act_msg=self.change_username(newname)
        exp_msg=self.expected_text('Update')['Title']
        print(f'exp:{exp_msg} VS. get:{act_msg}')
        assert exp_msg == act_msg
        self.click_popup_ok_btn()
        ### ellenőrízzük, hogy a névváltoztatás megjelenik-e a menüsoron is
        navbar_items = self.locate_navbar_items()
        check_newname = navbar_items[-2].text
        assert check_newname == newname



    # TC9: Adat vagy adatok törlése----------------------------------------------------------------------------------------------------------
    # Először létrehozunk egy új cikket, majd töröljük,
    # azt ellenőrizzük, hogy a saját listázott cikkeink száma törlést követően 1-el csökkent
    @allure.id('TC9. P+')
    @allure.title('Új cikk felvétele és törlése')
    def test_delete_data(self):
        self.signin_rutin()

        self.use_new_article_btn()
        new_article = self.new_article_dict()
        self.create_new_article(new_article)

        users_articles=self.sajat_cikkek()
        NR_before_D=len(users_articles)

        users_articles[-1].click()
        self.use_delete_article_btn()
        # time.sleep(5)
        # self.browser.refresh()
        users_articles_now=self.sajat_cikkek()
        NR_after_D = len(users_articles_now)

        print(f'before={NR_before_D}-1 == after={NR_after_D}')
        assert NR_before_D-1 == NR_after_D


    # TC10:	Adatok lementése felületről------------------------------------------------------------------------------------------------------

    # TC11:	Kijelentkezés--------------------------------------------------------------------------------------------------------------------
    # Miután ellenőriztük, hogy belépett státuszban vagyunk: kilépünk
    # A Kilépés sikerességét a menűsor változásával/a belépés gomb jelenlétével ellenőrizzük
    @allure.id('TC11. P+')
    @allure.title('Kilépés sikerességének ellenőrzése')
    def test_sign_out(self):
        self.signin_rutin()

        time.sleep(2)
        self.browser.refresh()
        navbar_items = self.locate_navbar_items()
        menusor_hossz = len(navbar_items)

        if menusor_hossz == 5:  # sikeres belépés
            assert menusor_hossz == 5
            print(f'\nMenuelemek száma: {menusor_hossz} -> Belépés megvalósult!')
            logout_btn = self.log_out_btn()
            logout_btn.click()

        # self.browser.refresh()
        navbar_items = self.locate_navbar_items()
        menusor_hossz = len(navbar_items)
        if menusor_hossz == 3:  # sikeres kilépés
            assert menusor_hossz == 3
            print(f'Menuelemek száma: {menusor_hossz} -> Kilépés megvalósult!')
            login_btn = self.log_in_btn()
            assert login_btn
            ### assert "Log out" felírat meglétének ellenőrzésével
            sign_in_btn_txt = navbar_items[-2].text
            assert sign_in_btn_txt == 'Sign in'
            print(f'Igazolt kilépés: "{sign_in_btn_txt}" gombfelírat megjelent!')
