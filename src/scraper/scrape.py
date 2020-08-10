from bs4 import BeautifulSoup
import requests as rq
import re
import json
import argparse


homepage = 'https://keurmerkenwijzer.nl/keurmerken/'
quality_levels = {'Zeer laag': 0, 'Laag': 1, 'Matig': 2, 'Redelijk': 3, 'Hoog': 4, 'Zeer hoog': 5,
                  'Nader te bepalen': 'N.t.b.', 'Niet van toepassing': 'N.v.t.', 'Zie omschrijving': 'Z.o.'}


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
        info[label.lower()] = quality_levels[score]

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


def main(quality_mark, category):
    quality_mark_url = quality_mark + '-' + category
    info = scrape_quality_mark_info(quality_mark_url)
    # print(info)
    return info


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('qm', type=str, help='quality mark name')
    parser.add_argument('cat', type=str, help='category')
    args = parser.parse_args()
    main(args.qm, args.cat)
