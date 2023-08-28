import requests
from bs4 import BeautifulSoup

url = 'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/'

response = requests.get(url)

html_text = requests.get(url).text

soup = BeautifulSoup(html_text, 'html.parser')

data = soup.find_all("table", {'class': 'cal'})


def parser_calendar():
    calendar = {}
    month_number = 1

    for i in data:
        month = [x.text.strip() for x in i.find_all('th') if 'month' in str(x)]
        holiday = [int(x.text.strip().replace('*', '')) for x in i.find_all('td') if 'holiday' in str(x)]
        weekend = [int(x.text.strip()) for x in i.find_all('td') if 'weekend' in str(x) and 'holiday' not in str(x)]
        work = [int(x.text.strip()) for x in i.find_all('td') if
                '' in str(x) and 'inactively' not in str(x) and 'holiday' not in str(x) and 'weekend' not in str(x)]
        calendar.update({month[0]: {'work': work, 'holiday': holiday, 'weekend': weekend}})
        month_number += 1

    return calendar


def check_day(mount, day, data):
    key_day = ['work', 'holiday', 'weekend']
    if mount in data:
        res = data[mount]
        for key in key_day:
            if day in res[key]:
                return key
    return ("Элемент не найден")


def main(mount, day):
    data = parser_calendar()
    result = check_day(mount, day, data)
    return result


if __name__ == "__main__":
    mount = input("enter month -> ")
    day = int(input("enter day -> "))
    print(main(mount, day))





