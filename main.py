import requests
import lxml
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

oppers = ["мегафон", "tele2", "мтс", "билайн"]

ua = UserAgent()

http_proxy = "http://195.135.242.141:8081"

proxies = {
    'http': http_proxy,
    # 'https': https_proxy,
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': ua.random,
}


def file_edit(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        li = [item for item in file.read().split('\n')]

    ready_numbers = []

    for phone_number in li:
        ready_numbers.append(f'{phone_number} - {get_opp(phone_number)}')
        with open(file_name, 'w', encoding='utf-8') as file:
            for item in ready_numbers:
                file.write(f'{item}\n')


def get_opp(phone_number) -> str:
    data = {
        'number': f'{phone_number}',
    }

    try:
        response = requests.post("https://www.kody.su/check-tel", headers=headers,
                                 data=data, proxies=proxies)
        html = response.text

        soup = BeautifulSoup(html, "lxml")
        content_in = soup.find("div", class_="content__in").text.lower()
        for opp in oppers:
            if opp in content_in:
                return f'{opp.capitalize()}'
        else:
            return f'Другие'
    except Exception as ex:
        print(ex)
        return


if __name__ == '__main__':
    file_edit('1')
