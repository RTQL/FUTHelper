from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as Bs
import sqlite3
from login_pass import ea_login, ea_password
import unicodedata
from urllib.parse import unquote


options = Options()
options.page_load_strategy = 'eager'
options.add_argument(
    "user-agent="
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/66.0.3359.181 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
serv = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=serv, options=options)

driver.get('https://www.ea.com/en-en/fifa/ultimate-team/web-app/')
time.sleep(7)
driver.find_element(By.XPATH, '//*[@id="Login"]/div/div/button[1]').click()
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(ea_login)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(ea_password)
driver.find_element(By.XPATH, '//*[@id="logInBtn"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="btnSendCode"]').click()
txt = input('продолжить? y or any ')

if txt == 'y':
    driver.find_element(By.XPATH, '//html/body/main/section/nav/button[5]').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/main/section/section/div[2]/div/div/div[1]').click()
    time.sleep(2)
    check = 1
    club = {}
    while check == 1:
        html = driver.page_source
        soup = Bs(html, 'lxml')
        cards = soup.find_all('li', class_='listFUTItem')
        for card in cards:
            trade = card.find('div', class_='name').attrs['class'][-1].replace('name', 'trade')
            ovr = card.find('div', class_='rating').text
            pos = card.find('div', class_='position').text
            name = card.find('div', class_='name').text
            unquoted = unquote(name)  # нормализация имени к латинице
            norm_text = unicodedata.normalize('NFD', unquoted)
            shaved = ''.join(x for x in norm_text if not unicodedata.combining(x))
            name = unicodedata.normalize('NFC', shaved)
            pac = card.find_all('span', class_='value')[0].text
            sho = card.find_all('span', class_='value')[1].text
            pas = card.find_all('span', class_='value')[2].text
            dri = card.find_all('span', class_='value')[3].text
            _def = card.find_all('span', class_='value')[4].text
            phy = card.find_all('span', class_='value')[5].text
            guid = f"{ovr}{pos}_{name}_{pac}{sho}{pas}{dri}{_def}{phy}"
            club.update({guid: {name: trade}})
        try:
            next_button = '/html/body/main/section/section/div[2]/div/div/div/div[3]/div/button[2]'
            driver.find_element(By.XPATH, next_button).click()
            time.sleep(1)
        except:
            check = 0
            driver.close()
    cards = []
    for c in club.items():
        values = c[1]
        card = []
        card.append(c[0])
        for k, v in values.items():
            card.append(k)
            card.append(v)
        cards.append(card)
    connect = sqlite3.connect('../db/players_db.db')
    cursor = connect.cursor()
    cursor.execute(f"drop table if exists my_club")
    cursor.execute(f"create table if not exists my_club (guid primary key, name, trade_untrade)")
    for card in cards:
        cursor.execute(f"insert into my_club values{tuple(card)}")
    connect.commit()
    connect.close()
else:
    driver.close()
