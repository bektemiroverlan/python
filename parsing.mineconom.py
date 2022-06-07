import requests
from bs4 import BeautifulSoup 

MAIN_URL = 'http://mineconom.gov.kg/ru/vacancy'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'

def open_page(url):
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url)
    return response.text

def analize_page_content(content):
    soup = BeautifulSoup(content, 'lxml')
    return soup

def get_vacancy_cards(soup):
    list_ = soup.find('ul', class_ = 'list-unstyled posts')
    vacancy_card = list_.find_all('div', class_= 'media posts-list-item')
    return vacancy_card

def main():
    pages_count = 6
    all_vacancy_cards = []
    for page in range(1, pages_count + 1):
        url = f'{MAIN_URL}?page={page}'
        page_content = open_page(url)
        soup = analize_page_content(page_content)
        vacancy_cards = get_vacancy_cards(soup)
        all_vacancy_cards.extend(vacancy_cards)
    total_info = []
    for vacancy_card in all_vacancy_cards:
        vacancy_info = get_vacancy_info(vacancy_card)
        total_info.append(vacancy_info)
    print(total_info)
    write_to_csv(total_info)

def get_vacancy_info(vacancy_card):
    time_ = vacancy_card.find('div', class_='posts-list-item-date align-self-center mr-3')
    time = time_.text.strip()
    title_ = vacancy_card.find('div', class_='posts-list-item-title')
    title = title_.text.strip()

    info = {
        'time': time,
        'title': title
    }
    return info

def write_to_csv(data):
    '''Записывает данные в csv файл'''
    import csv
    with open('Mineconom.csv', 'w', encoding='utf-8') as file:
        fieldnames = ['time', 'title']
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        writer.writeheader()
        for product in data:
            writer.writerow(product)

if __name__ == '__main__':
    main()