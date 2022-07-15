import requests
import lxml
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

oppers = ["мегафон", "tele2", "мтс", "билайн"]


def get_opp(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        li = [item for item in file.read().split('\n')]

    ready_numbers = []

    ua = UserAgent()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': ua.random,
    }

    for phone_number in li:
        data = {
            'number': f'{phone_number}',
        }

        try:
            response = requests.post("https://www.kody.su/check-tel", headers=headers,
                                     data=data)
            html = response.text

            soup = BeautifulSoup(html, "lxml")
            content_in = soup.find("div", class_="content__in").text.lower()
            for opp in oppers:
                if opp in content_in:
                    ready_numbers.append(f'{phone_number} - {opp.capitalize()}')
                    break
            else:
                ready_numbers.append(f'{phone_number} - Другие')
        except Exception as ex:
            print(ex)

        with open(file_name, 'w', encoding='utf-8') as file:
            for item in ready_numbers:
                file.write(f'{item}\n')


if __name__ == '__main__':
    get_opp('1')

