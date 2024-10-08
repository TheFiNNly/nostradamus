import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class Signin:  # класс для авторизации на сайте
    def __init__(self, login='mag.vladislav@mail.ru', password='199536688VlAd'):
        global driver
        driver = webdriver.Chrome()  # создаем подключение
        driver.maximize_window()

        driver.get("https://smart-tables.ru/login")
        time.sleep(3)

        self.username_field = driver.find_element(By.CSS_SELECTOR, '#email')
        self.password_field = driver.find_element(By.CSS_SELECTOR, '#password')
        self.login_button = driver.find_element(By.CSS_SELECTOR, '#__layout > div > div.content-page > main > '
                                                                 'div > div.row.justify-content-center > div > div > '
                                                                 'div > form > div.form-group.mb-0.text-center > '
                                                                 'button.btn.btn-primary')

        self.username_field.send_keys(login)
        self.password_field.send_keys(password)
        self.login_button.click()
        time.sleep(3)

        self.cookies = driver.get_cookies()
        for cookie in self.cookies:
            driver.add_cookie(cookie)


class GetTeams:  # класс для парсинга всех команд посезонно
    def __init__(self):
        Signin()
        self.table = None
        self.teams = []
        self.url = f'https://smart-tables.ru/league/Netherlands/Eredivisie'  # для АПЛ
        driver.get(self.url)
        time.sleep(3)

        # выбираем все сезоны
        self.seasons = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/div[1]/'
                                                     'div[2]/div[1]/div/div[1]/div[2]/div[1]/button[9]')

        # устанавливаем число матчей
        self.matches_count = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/div[1]/'
                                                           'div[2]/div[1]/div/div[1]/div[5]/button[9]')
        self.matches = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/div[1]/'
                                                     'div[2]/div[1]/div/div[1]/div[5]/button[9]/input')

        # кнопка обновления
        self.refresh_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/'
                                                            'div[1]/div[2]/div[1]/div/button')

    def teams_table(self):
        self.seasons.click()
        self.matches_count.click()
        self.matches.clear()
        self.matches.send_keys('1000')
        self.refresh_button.click()

        time.sleep(3)

        self.table = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/div[1]/'
                                                   'div[2]/div[2]/div/div[2]/table/tbody').text
        self.table = self.table.splitlines()
        for i in self.table:
            i = i.split()
            if i[2].isalpha():
                self.teams.append(i[1].lower() + '_' + i[2].lower())
            else:
                self.teams.append(i[1].lower())
        driver.quit()
        return self.teams


class GetStats:  # класс для парсинга статистики по каждой команде
    def __init__(self, team, champ):
        #  авторизируемся и открываем url с нужной командой
        Signin()
        self.result_total, self.result_goals, self.result_stats = [], [], []
        self.table, self.transform = None, None
        self.team = team
        self.champ = champ
        self.url = f'https://smart-tables.ru/team/{team}'
        driver.get(self.url)
        time.sleep(3)

        # все сезоны
        self.season = driver.find_element(By.CSS_SELECTOR, '#teamsSeasons')
        self.season.find_elements(By.XPATH, ".//*")[-1].click()
        time.sleep(2)

        #  количество матчей
        driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div[4]/div[2]/div[1]/div/div[1]/'
                                      'div[6]/button[9]').click()
        self.season_matches = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/'
                                                            'div[2]/div[1]/div/div[1]/div[6]/button[9]/input')
        self.season_matches.clear()
        self.season_matches.send_keys('1000')
        time.sleep(2)

        # премьер-лига
        self.league = driver.find_element(By.CSS_SELECTOR, '#refCompetitions')
        self.league.find_elements(By.XPATH, ".//*")[-1].click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Eredivisie')]").click()

        # кнопка голов
        self.goals_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div[4]/div[2]/'
                                                          'div[1]/div/div[1]/div[1]/div[1]/button[1]')

        # кнопка xG
        self.xg_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div[4]/div[2]/'
                                                       'div[1]/div/div[1]/div[1]/div[1]/button[2]')

        # кнопка corners
        self.corners_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/div[2]/'
                                                            'div[1]/div/div[1]/div[1]/div[1]/button[3]')

        # кнопка офсайда
        self.offside_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/div[2]/'
                                                            'div[1]/div/div[1]/div[1]/div[1]/button[5]')

        # кнопка фолов
        self.fouls_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/div[2]/'
                                                          'div[1]/div/div[1]/div[1]/div[1]/button[6]')

        # кнопка ударов в створ
        self.shots_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/div[2]/'
                                                          'div[1]/div/div[1]/div[1]/div[1]/button[7]')

        # кнопка атак
        self.attack_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[4]/div[2]'
                                                           '/div[1]/div/div[1]/div[1]/div[1]/button[9]')

        # кнопка выпадающего списка
        self.dropdown = driver.find_element(By.CSS_SELECTOR, '#filterTypeStat')
        self.dropdown.click()
        time.sleep(3)

        # кнопка владения (из dropdown)
        self.possession = driver.find_element(By.CSS_SELECTOR,
                                              '#__layout > div > div > main > div > div:nth-child(4) > '
                                              'div.col-lg-8 > div:nth-child(1) > div > div.filter-base > '
                                              'div.btn-group.py-1.mr-2.stat-picker > '
                                              'div.btn-group.stat-picker-desktop.show > div > a:nth-child(2)')

        # кнопка КК (из dropdown)
        self.redcard = driver.find_element(By.CSS_SELECTOR,
                                           '#__layout > div > div > main > div > div:nth-child(4) > '
                                           'div.col-lg-8 > div:nth-child(1) > div > div.filter-base > '
                                           'div.btn-group.py-1.mr-2.stat-picker > '
                                           'div.btn-group.stat-picker-desktop.show > div > a:nth-child(3)')

        # кнопка передач (из dropdown)
        self.passes = driver.find_element(By.CSS_SELECTOR,
                                          '#__layout > div > div > main > div > div:nth-child(4) > '
                                          'div.col-lg-8 > div:nth-child(1) > div > div.filter-base > '
                                          'div.btn-group.py-1.mr-2.stat-picker > '
                                          'div.btn-group.stat-picker-desktop.show > div > a:nth-child(5)')

        # кнопка сейвов (из dropdown)
        self.saves = driver.find_element(By.CSS_SELECTOR,
                                         '#__layout > div > div > main > div > div:nth-child(4) > '
                                         'div.col-lg-8 > div:nth-child(1) > div > div.filter-base > '
                                         'div.btn-group.py-1.mr-2.stat-picker > '
                                         'div.btn-group.stat-picker-desktop.show > div > a:nth-child(6)')

        # кнопка точность передач (из dropdown)
        self.pass_acc = driver.find_element(By.CSS_SELECTOR,
                                            '#__layout > div > div > main > div > div:nth-child(4) > '
                                            'div.col-lg-8 > div:nth-child(1) > div > div.filter-base > '
                                            'div.btn-group.py-1.mr-2.stat-picker > '
                                            'div.btn-group.stat-picker-desktop.show > div > a:nth-child(14)')

        # кнопка отборов (из dropdown)
        self.tacking = driver.find_element(By.CSS_SELECTOR,
                                           '#__layout > div > div > main > div > div:nth-child(4) > '
                                           'div.col-lg-8 > div:nth-child(1) > div > div.filter-base > '
                                           'div.btn-group.py-1.mr-2.stat-picker > '
                                           'div.btn-group.stat-picker-desktop.show > div > a:nth-child(19)')

        # кнопка обновления
        self.refresh_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div[4]/'
                                                            'div[2]/div[1]/div/button')

        # кнопки параметров (вне dropdown)
        self.param_list = [self.xg_button, self.corners_button, self.offside_button, self.fouls_button,
                           self.shots_button, self.attack_button]

        # кнопки параметров (dropdown)
        self.param_list_dropdown = [self.possession, self.redcard, self.passes, self.saves, self.pass_acc, self.tacking]

    def transformer(self, data):
        transform = data.split(self.champ)
        res_transform = []
        for i in transform:
            if len(i) > 2:
                x = i.split()
                res_transform.append(x)
        return res_transform

    def regulator(self):
        # 1 - чемпионат; 2 - дата; 3 - команда 1; 4 - голы команды 1; 5 - команда 2; 6 - голы команды 2;
        # 7 - xg команды 1; 8 - xg команды 2; 9 - угловые команды 1; 10 - угловые команды 2; 11 - офсайды команды 1;
        # 12 - офсайды команды 2; 13 - фолы команды 1; 14 - фолы команды 2; 15 - удары команды 1;  16 - удары команды 2;
        # 17 - атаки команды 1; 18 - атаки команды 2; 19 - владение команды 1; 20 - владение команды 2;
        # 21 - КК команды 1; 22 - КК команды 2; 23 - передачи команды 1; 24 - передачи команды 2; 25 - сейвы команды 1;
        # 26 - сейвы команды 2; 27 - точность передач команды 1; 28 - точность передач команды 2; 29 - отборы команды 1;
        # 30 - отборы команды 2;

        for match in GetStats.goals(self):
            if match[3].isdigit() and match[6].isdigit():
                team1, team2, value1, value2 = match[2], match[5], match[3], match[4]
            elif match[3].isalpha() and match[7].isdigit():
                team1, team2, value1, value2 = match[2] + '_' + match[3], match[6], match[4], match[5]
            elif match[3].isdigit() and match[6].isalpha():
                team1, team2, value1, value2 = match[2], match[5] + '_' + match[6], match[3], match[4]
            else:
                team1, team2, value1, value2 = match[2] + '_' + match[3], match[6] + '_' + match[7], match[4], \
                    match[5]
            self.result_total.append([self.champ, match[1] + '.' + '20' + match[0][4:6], team1, value1, team2, value2])

        # перебор параметров
        for param in self.param_list:
            for match, i in zip(GetStats.stats_param(self, param), range(len(self.result_total))):
                if match[3][0].isdigit():
                    value1, value2 = match[3], match[4]
                else:
                    value1, value2 = match[4], match[5]
                self.result_total[i].extend([value1, value2])

        # перебор параметров dropdown
        for param in self.param_list_dropdown:
            for match, i in zip(GetStats.stats_param_dropdown(self, param), range(len(self.result_total))):
                if match[3][0].isdigit():
                    value1, value2 = match[3], match[4]
                else:
                    value1, value2 = match[4], match[5]
                self.result_total[i].extend([value1, value2])

        driver.quit()
        return self.result_total

    def goals(self):
        # голы
        self.goals_button.click()
        self.refresh_button.click()
        time.sleep(3)

        self.table = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div[4]/div[2]/'
                                                   'div[2]/div/table[4]/tbody').text
        self.result_goals = self.transformer(self.table)
        return self.result_goals

    def stats_param(self, param):
        param.click()
        self.refresh_button.click()
        time.sleep(3)

        self.table = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div[4]/div[2]/'
                                                   'div[2]/div/table[4]/tbody').text

        self.result_stats = self.transformer(self.table)
        return self.result_stats

    def stats_param_dropdown(self, param):
        self.goals_button.click()
        self.refresh_button.click()
        time.sleep(3)

        self.dropdown.click()
        param.click()
        self.refresh_button.click()
        time.sleep(3)

        self.table = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div[4]/div[2]/'
                                                   'div[2]/div/table[4]/tbody').text

        self.result_stats = self.transformer(self.table)
        return self.result_stats
