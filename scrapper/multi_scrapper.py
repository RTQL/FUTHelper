import json
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from timeit import default_timer as timer
from multiprocessing import Pool
import undetected_chromedriver as uc
import unicodedata
from urllib.parse import unquote

fifa_version = 22


def final_page():
    options = Options()
    options.page_load_strategy = 'eager'
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.get(f'https://www.futbin.com/{fifa_version}/latest')
    soup = Bs(driver.page_source, 'lxml')
    final_page = soup.find('tr', class_='player_tr_1').find('a').attrs['href'].split('/')[3]
    driver.close()
    print(f"{final_page} is final page")
    return int(final_page)


def multi_browser(_pages):
    options = Options()
    options.page_load_strategy = 'eager'
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = uc.Chrome(options=options, use_subprocess=True)
    datas = {}
    _errors = []
    for page in _pages:
        try:
            driver.get(page)
            soup = Bs(driver.page_source, 'lxml')
            futbin_id = page.split('player/')[1]
            keys = []
            values = []
            headers = soup.find_all('th')
            for h in headers:
                header = h.get_text().strip().replace('.', '').lower().replace(' ', '_')
                keys.append(header)
            infos = soup.find_all('td', class_='table-row-text')
            for info in infos:
                info = info.get_text().split('cm |')[0].strip().lower()
                values.append(info)
            main_stats = soup.find('div', class_='stats-inner').find('div', class_='row').find_all('div', class_='main_stat')
            for s in main_stats:
                main_stat = s.find_all('div')[0].get_text().strip().lower()
                keys.append(f"_{main_stat}")
            main_values = soup.find('div', class_='stats-inner').find('div', class_='row').find_all('div', class_='main_stat')
            guid_numbers = ''
            for v in main_values:
                main_value = v.find_all('div')[1].get_text().strip().lower()
                guid_numbers += str(main_value)
                values.append(main_value)
            overall = soup.find('div', class_='pcdisplay-rat').get_text().strip()
            card_name = soup.find('div', class_='pcdisplay-name').get_text().strip()
            if card_name == '':
                card_name = soup.find('title').get_text().split(' FIFA')[0].strip()
            unquoted = unquote(card_name)  # нормализация имени к латинице
            norm_text = unicodedata.normalize('NFD', unquoted)
            shaved = ''.join(x for x in norm_text if not unicodedata.combining(x))
            card_name = unicodedata.normalize('NFC', shaved)
            position = soup.find('div', class_='pcdisplay-pos').get_text().strip()
            card_type = soup.find('div', id='Player-card').attrs['data-revision']
            card_level = soup.find('div', id='Player-card').attrs['data-level']
            card_rarity = soup.find('div', id='Player-card').attrs['data-rare-type']
            trait_content = soup.find_all('div', class_='trait-name-val')
            traits = ''
            for t in trait_content:
                traits += t.get_text().strip() + ','
            traits = traits.strip(',')
            if card_rarity == str(0):
                card_rarity = 'non-rare'
            elif card_rarity == str(1):
                card_rarity = 'rare'
            else:
                card_rarity = 'special'
            guid = f"{overall + position}_{card_name}_{guid_numbers}"
            card = {
                'guid': guid,
                'futbin_id': futbin_id,
                'guid': guid,
                'overall': overall,
                'card_name': card_name,
                'position': position,
                'card_type': card_type,
                'card_level': card_level,
                'card_rarity': card_rarity,
                'traits': traits,
            }

            sub_stats = soup.find('div', class_='stats-inner').find('div', class_='row').find_all('div', class_='stat_holder_sub')
            for s in sub_stats:
                sub_stat = s.get_text().strip().replace('.', '').lower().replace(' ', '_')
                keys.append(sub_stat)
            sub_values = soup.find('div', class_='stats-inner').find('div', class_='row').find_all('div', class_='sub_stat')
            for v in sub_values:
                sub_value = v.find('div', id=True).get_text().strip()
                values.append(sub_value)
            stats = dict(zip(keys, values))
            card.update(stats)
            datas.update({guid: card})
            # print(f"{futbin_id} is scrapped")
        except Exception as ex:
            check = soup.find('div').get_text().strip().split(' ')[0]
            if check != "We're":
                # print(f'error {futbin_id}')
                _errors.append(page)
            pass
    driver.close()
    return {
        'data': datas,
        'errors': _errors
    }


if __name__ == '__main__':
    start = timer()
    futbin_final_page = final_page()
    data = {}
    try:
        with open('last_page.json', 'r') as file:
            last_page = int(json.load(file)['id'])
    except:
        last_page = 1
    if futbin_final_page == last_page:
        print('Database is fresh! No data for update')
    else:
        try:
            with open('../db/data.json', 'r') as file:
                data.update(json.load(file))
        except:
            pass
        start = timer()
        pages_first = []
        pages_second = []
        pages_third = []
        pages_fourth = []
        pages_fifth = []
        pages_sixth = []
        pages_seventh = []
        pages_eighth = []
        count = 1
        for x in range(last_page, futbin_final_page + 1):
            if count == 1:
                pages_first.append(f'https://www.futbin.com/{fifa_version}/player/{x}')
                count += 1
            elif count == 2:
                pages_second.append(f'https://www.futbin.com//{fifa_version}/player/{x}')
                count += 1
            elif count == 3:
                pages_third.append(f'https://www.futbin.com/{fifa_version}/player/{x}')
                count += 1
            elif count == 4:
                pages_fourth.append(f'https://www.futbin.com/{fifa_version}/player/{x}')
                count += 1
            elif count == 5:
                pages_fifth.append(f'https://www.futbin.com/{fifa_version}/player/{x}')
            #     count += 1
            # elif count == 6:
            #     pages_sixth.append(f'https://www.futbin.com/{fifa_version}/player/{x}')
            #     count += 1
            # elif count == 7:
            #     pages_seventh.append(f'https://www.futbin.com/{fifa_version}/player/{x}')
            #     count += 1
            # elif count == 8:
            #     pages_eighth.append(f'https://www.futbin.com/{fifa_version}/player/{x}')
                count = 1
        pages = [pages_first, pages_second, pages_third, pages_fourth, pages_fifth,
                 # pages_sixth, pages_seventh, pages_eighth,
                 ]
        counter = 0
        for p in pages:
            counter += len(p)
        print(f"total {counter} pages for scan")
        pool = Pool(len(pages))
        result = pool.map(multi_browser, pages)
        errors = []
        for lst in result:
            data.update(lst['data'])
        for lst in result:
            errors.append(lst['errors'])
        for e in errors[0:]:
            errors += e
            errors.pop(0)

        print(errors)
        if len(errors) > 0:
            print('errors recycling')
            result = multi_browser(errors)
            for lst in result:
                data.update(result['data'])
        errors = []
        try:
            for lst in result:
                errors.append(result['errors'])
            for e in errors[0:]:
                errors += e
                errors.pop(0)
        except:
            pass
        print(errors)
        if len(errors) == 0:
            print('success!')
        else:
            print('something wrong!')

        with open('../db/data.json', 'w') as file:
            json.dump(data, file, indent=4)

        max_value = 0
        for card in data.values():
            if int(card['futbin_id']) >= max_value:
                max_value = int(card['futbin_id'])
        with open('last_page.json', 'w') as file:
            json.dump({'id': max_value}, file)
    end = timer()
    time = end - start
    print(f"\nTime taken: {time}\nTotal: {len(data)} pages scanned\nSpeed: {len(data) / time} pages per sec")
