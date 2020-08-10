from bs4 import BeautifulSoup
import requests
import numpy as np
import json


def categorieen_ophalen():
    """deze functie scraped de verschillende categoriën van de homepage"""
    categories_all = []
    url = 'https://keurmerkenwijzer.nl/alle-categorieen/'
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, 'html.parser')
    results = content.findAll('h3', attrs={'class': "product-category__title"})
    for row in results:
        categories_all.append(row.text)
    categories_url = []
    for cat in categories_all:
        cat = cat.replace(' ', '-').replace(",", "").lower()
        url1 = 'https://keurmerkenwijzer.nl/overzicht/'
        url = url1+cat
        categories_url.append(url)
    return categories_url


def getting_names(categories_url):
    """op basis van de gescrapte categorieeën worden de bijbehorende merken opgehaald"""
    keurmerken = []
    links_keurmerken = []
    for element in categories_url:
        url = element
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser")
        alle_keurmerken = content.findAll('h2', attrs={'class': "quality-mark__title h4"})
        for k in alle_keurmerken:
            keurmerken.append(k.text)
        alle_links = content.findAll('a', attrs={'class': "quality-mark__link"})
        for i in range(len(alle_links)):
            one_a_tag = alle_links[i]
            link = one_a_tag["href"]
            links_keurmerken.append('https://keurmerkenwijzer.nl' + link)
    return keurmerken, links_keurmerken


# getting info on the keurmerken.
def counting_green_bars(content, command):
    """van elke keurmerk wordt de ranking opgehaald die in de groene balkjes in de website zitten"""
    ratings = np.str(content.findAll('div', attrs={'class': 'tooltip tooltip--dark tooltip--center'}))
    ratings = ratings.split('/div>, <div class="tooltip tooltip--dark tooltip--center')[0:5]
    commands = {
        'milieu': 0,
        'dier': 1,
        'mens': 2,
        'controle': 3,
        'transparantie': 4
    }
    score = ratings[commands[command]]
    rankings = ['Hoog', 'Nader te bepalen', 'Zie omschrijving', 'Zeer hoog',
                'Niet van toepassing', 'Redelijk', 'Matig', 'Laag',
                'Zeer laag']
    for r in rankings:
        if r in score:
            status = r
            break
    return status


def getting_info(links_keurmerken, keurmerken):
    """elke webpage van een keurmerk wordt gescraped en toegevoegd aan een object"""
    keurmerkArr = []
    for i in range(len(links_keurmerken)):
        name_keurmerk = keurmerken[i]
        url = links_keurmerken[i]
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser")
        # sommige keurmerken hebben niet alle info, dus als er een error komt
        # omdat het item leeg is, wordt er een lege string neer gezet
        try:
           kwali = content.find('span', attrs={'class': "quality-mark-type__label"}).text.strip()
        except AttributeError:
           kwali = ""
        try:
            site = content.find('a', attrs = {'class': 'info-block__content'})["title"]
        except TypeError:
            site = ""
        try:
            screening = content.find('a', attrs={'class': 'link last-screen__link'}).text
        except AttributeError:
            screening = ""
        beschrijving = content.find('p').text
        beschrijving = np.str(beschrijving).split('\r\n')[0].replace('\u00a0', "")
        keurmerkObject = {
            "keurmerk": name_keurmerk,
            "categorie": content.find('a', attrs={'class': "breadcrumb__item"}).text,
            'beschrijving': beschrijving,
            'image': 'https://keurmerkenwijzer.nl/'+ content.find('img')['src'],
            "kwaliteit": kwali,
            "last_screening": screening,
            "website": site,
            "ratings": [
                {
                "milieu": counting_green_bars(content, "milieu"),
                "dierenwelzijn": counting_green_bars(content, "dier"),
                "mens&werk": counting_green_bars(content, "mens"),
                "controle": counting_green_bars(content, "controle"),
                "transparantie": counting_green_bars(content, "transparantie")
                }
            ]
        }
        keurmerkArr.append(keurmerkObject)
    return keurmerkArr


def testing(goal, keurmerkArr):
    """het testen of een keurmerk naam in de gescrapte data staat"""
    found = 0
    for i in range(len(keurmerkArr)):
        if goal in keurmerkArr[i]['keurmerk']:
            found = 1
    if found != 1:
        print('Aow, not found')


def test_cases(keurmerkArr):
    """verschillende test cases"""
    testing('EU Ecolabel Toerisme', keurmerkArr)
    testing('Dolphin Safe', keurmerkArr)
    testing('COSMOS Natural (BDIH)', keurmerkArr)
    testing('Weidemelk', keurmerkArr)
    testing('VCS Klimaatcompensatie', keurmerkArr)


def main():
    categories_url = categorieen_ophalen()
    keurmerken, links_keurmerken = getting_names(categories_url)
    keurmerkArr = getting_info(links_keurmerken, keurmerken)
    test_cases(keurmerkArr)
    with open("keurmerkData.json", "w") as outfile:
        json.dump(keurmerkArr, outfile)


if __name__ == '__main__':
    main()