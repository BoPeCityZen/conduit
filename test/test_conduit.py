import csv
import time
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from conduit_functions import callFunctions


class Test11ConduitFunction(callFunctions):

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

    def teardown_method(self):
        self.browser.quit()

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
        if actual_str['swal_title'] == expected_str['Title']:
            assert actual_str['swal_title'] == expected_str['Title']
            assert actual_str['swal_text'] == expected_str['Text']
            print(f"Assert a pozitív ágon: {actual_str['swal_title']} ({actual_str['swal_text']})")
        else:
            print('Localhost-on fontos, hogy a "Pass" dictionary-ből meghívott useradatokkal történt-e már regisztráció')


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
        GiveNewArTitle = self.create_new_article(new_article)

        DispArTitle = self.Article_title_field().text
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

                DispArTitle = self.Article_title_field().text
                ### Ellenőrizzük a megjelenő cikk címezejét, hogy egyezik-e a beküldött címadattal
                print(f'Bevitt cím-->> {GiveNewArTitle} <Vs> {DispArTitle} <<--megjelenő cím')
                assert DispArTitle == GiveNewArTitle

    # TC8: Meglévő adat módosítás------------------------------------------------------------------------------------------------------------
    @allure.id('TC8. P+')
    @allure.title('Meglévő adat módosítás')
    def test_update_data(self):
        username = self.signin_rutin()
        newname = f'BrandNew{username}'
        self.use_settings_btn()
        ### elvégezzük a névváltoztatást és ellenőrizzük a visszaigazoló üzenetet kiszervezett funkcióban
        act_msg = self.change_username(newname)
        exp_msg = self.expected_text('Update')['Title']
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

        users_articles = self.sajat_cikkek()
        NR_before_D = len(users_articles)

        users_articles[-1].click()
        self.use_delete_article_btn()
        users_articles_now = self.sajat_cikkek()
        NR_after_D = len(users_articles_now)

        print(f'before={NR_before_D}-1 == after={NR_after_D}')
        assert NR_before_D - 1 == NR_after_D

    # TC10:	Adatok lementése felületről------------------------------------------------------------------------------------------------------
    @allure.id('TC10. P+')
    @allure.title('Adatlementés ellenőrzése')
    # Tag elemeket kigyűjtüm egy listába, majd kiírom egy fájlba,
    # Visszaolvasással azt ellenőrzőm, hogy a kíírt és a kigyűjtött elemek egyeznek-e
    def test_write_to_file(self):
        self.signin_rutin()
        actual_tags = self.tag_list()
        tagek = []
        for t in range(len(actual_tags)):
            tag_name = actual_tags[t].text
            tagek.append(tag_name)
            with open('test/tagek_ide.csv', 'w', encoding="utf8") as tag:
                writer = csv.writer(tag)
                writer.writerow(tagek)
        with open('test/tagek_ide.csv', 'r', encoding="utf8") as file:
            tags_from_csv = csv.reader(file, delimiter=',')
            csv_headings = next(tags_from_csv)
            for element in range(len(csv_headings)):
                print(f'(weblapról kigyűjtött) {actual_tags[element].text} <-Vs-> {csv_headings[element]} (fájlba kíírt) ')
                assert csv_headings[element] == actual_tags[element].text

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

        if menusor_hossz == 5:  ### sikeres belépés
            assert menusor_hossz == 5
            print(f'\nMenuelemek száma: {menusor_hossz} -> Belépés megvalósult!')
            logout_btn = self.log_out_btn()
            logout_btn.click()

        navbar_items = self.locate_navbar_items()
        menusor_hossz = len(navbar_items)
        if menusor_hossz == 3:  ### sikeres kilépés
            assert menusor_hossz == 3
            print(f'Menuelemek száma: {menusor_hossz} -> Kilépés megvalósult!')
            login_btn = self.log_in_btn()
            assert login_btn
            ### assert "Log out" felírat meglétének ellenőrzésével
            sign_in_btn_txt = navbar_items[-2].text
            assert sign_in_btn_txt == 'Sign in'
            print(f'Igazolt kilépés: "{sign_in_btn_txt}" gombfelírat megjelent!')
