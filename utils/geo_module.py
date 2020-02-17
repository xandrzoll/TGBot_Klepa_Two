import requests
from ..config import YA_KEY


BASE_URL = r'https://geocode-maps.yandex.ru/1.x/'


def get_geo_coordinates(adr):
    post_data = dict()
    post_data['apikey'] = YA_KEY
    post_data['format'] = 'json'
    post_data['geocode'] = adr

    try:
        r = requests.get(BASE_URL, post_data)
        pos = r.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    except Exception as err:
        pos = ''
        print(err)
    return pos


def load_addresses_geo():
    adrs = []
    with open(r'D:\projects\TGBot_Klepa_Two\utils\AddressBook.csv', 'r', encoding='utf-8') as f:
        for line in f.readlines()[1:]:
            if not line or line == '\n':
                continue
            adr = line.split(';')
            # adr[0] = int(adr[0])
            if adr[2] == '""' or not adr[2] or adr[2] == '0':
                geo = get_geo_coordinates(adr[1].replace('"', ''))
                if geo:
                    adr[2], adr[3] = geo.split()
            adrs.append(adr)

    with open(r'D:\projects\TGBot_Klepa_Two\utils\AddressBook.csv', 'w', encoding='utf-8') as f:
        f.write('"indx";"full_address_text";"lat";"lon"\n')
        for adr in adrs:
            f.write(';'.join(adr))
            f.write('\n')
    return adrs


if __name__ == '__main__':
    adrs = load_addresses_geo()
    print(adrs)
