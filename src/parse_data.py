from typing import Generator

import requests
from bs4 import BeautifulSoup

from config import DATA_URL_FOR_PARSER
from src.models import Item


def parse_page(url) -> Generator[list[str, int], None, None]:
    print('parse_page')
    response = requests.get(url)
    print('response:', response)
    soup = BeautifulSoup(response.text, 'html.parser')
    # noinspection SpellCheckingInspection
    bombardirs = soup.find('div', class_='search-block bombardir')
    table = bombardirs.find('table')

    if table:
        # noinspection SpellCheckingInspection
        rows = table.find_all('tr')[1:]  # Пропускаем заголовок таблицы
        # noinspection SpellCheckingInspection
        for row in rows:
            columns = row.find_all('td')
            position = int(columns[0].text)
            full_name = columns[2].text.strip()
            # Получаем ссылку на изображение логотипа команды
            logo_url = columns[4].find('img')['src']
            total_goals = int(columns[5].text)
            penalty_goals = int(columns[6].text)
            matches = int(columns[7].text)
            print(position, full_name, logo_url, total_goals, penalty_goals, matches)
            yield position, full_name, logo_url, total_goals, penalty_goals, matches
    else:
        # noinspection SpellCheckingInspection
        print("Таблица не найдена на странице.")


def get_data() -> list[list[str, int]]:
    print('url:', DATA_URL_FOR_PARSER)
    PARSED_PAGES = parse_page(DATA_URL_FOR_PARSER)

    DATA: list[list[str, int]] = [[]]
    for ROW in PARSED_PAGES:
        DATA.append(ROW)

    return DATA
