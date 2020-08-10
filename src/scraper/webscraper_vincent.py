from bs4 import BeautifulSoup
import requests as rq
import re
import json


homepage = 'https://keurmerkenwijzer.nl'
quality_levels = {'Zeer laag': 0, 'Laag': 1, 'Matig': 2, 'Redelijk': 3, 'Hoog': 4, 'Zeer hoog': 5,
                  'Nader te bepalen': 'N.t.b.', 'Niet van toepassing': 'N.v.t.', 'Zie omschrijving': 'Z.o.'}


def scrape_categories():
    """Scrape categories from the main page."""
    category_urls = []
    url = homepage + '/alle-categorieen/'
    response = rq.get(url, timeout=5)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_soup = soup.find('main')

    for category in main_soup.find_all('a', {'href':  re.compile(r'/overzicht/')}):
        category_urls.append(category['href'])

    return category_urls


def scrape_quality_marks(category_url):
    """Scrape quality mark names for a given category."""
    quality_mark_urls = []
    url = homepage + category_url
    response = rq.get(url, timeout=5)
    soup = BeautifulSoup(response.content, 'html.parser')

    for quality_mark in soup.find_all('div', {'class': 'quality-mark'}):
        quality_mark_url = quality_mark.find('a', {'class': 'quality-mark__link'})['href']
        quality_mark_urls.append(quality_mark_url)

    return quality_mark_urls


def scrape_quality_mark_info(quality_mark_url):
    """Scrape information for a given quality mark."""
    info = {}
    url = homepage + quality_mark_url
    response = rq.get(url, timeout=5)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_soup = soup.find('main')

    # Scrape name and logo
    info['name'] = main_soup.find('h1').text
    info['logo'] = homepage + main_soup.find('img')['src']

    # Scrape scores
    labels, scores = scrape_scores(main_soup)
    for label, score in zip(labels, scores):
        info[label] = quality_levels[score]

    # Scrape last screening date, mark_type and description
    info['screening'] = scrape_screening(main_soup)
    info['mark_type'] = scrape_mark_type(main_soup)
    info['description'] = scrape_description(main_soup)

    return info


def scrape_scores(main_soup):
    """Scrape the scores for a given quality mark soup."""
    ul = main_soup.find('ul', {'class': 'quality-mark-bar-list'})

    labels = []
    for li in ul.find_all('li'):
        label = str(li.text).strip()
        if label is not '' and '.' not in label:
            labels.append(label)

    scores = []
    for div in ul.find_all('div'):
        scores.append(div['data-tooltip-text'])

    return labels, scores


def scrape_screening(main_soup):
    """Scrape the last screening date for a given quality mark soup."""
    screening = main_soup.find('a', {'class': 'last-screen__link'})

    if screening:
        screening = screening.text
    else:
        screening = 'N.t.b.'

    return screening


def scrape_mark_type(main_soup):
    """Scrape the mark type for a given quality mark main soup."""
    mark_type = main_soup.find('span', {'class': 'quality-mark-type__label'})

    if mark_type:
        mark_type = mark_type.text.strip()
    else:
        mark_type = 'N.t.b.'

    return mark_type


def scrape_description(main_soup):
    """Scrape the description for a given quality mark main soup."""
    rich_text = main_soup.find('div', {'class': 'rich-text'})
    description = rich_text.find('p').text

    return description


def main():
    quality_marks = []
    category_urls = scrape_categories()

    for category_url in category_urls:
        quality_mark_urls = scrape_quality_marks(category_url)
        category = category_url.split('/')[-2]

        for quality_mark_url in quality_mark_urls:
            info = scrape_quality_mark_info(quality_mark_url)
            info['category'] = category
            quality_marks.append(info)

    with open('keurmerkData.json', 'w') as outfile:
        json.dump(quality_marks, outfile)


if __name__ == '__main__':
    main()
