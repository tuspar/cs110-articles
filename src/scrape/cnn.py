import scraper

def get_links_2019() -> list[str]:
    '''
    Returns a list of the top 100 CNN articles from 2019
    '''
    url = "https://www.cnn.com/2019/12/22/us/top-100-digital-stories-2019-trnd/index.html"
    cnn2019 = scraper.get(url)

    links = []
    for paragraph in scraper.find_all('p', cnn2019):
        for link in scraper.find_all('a', paragraph['element']):
            if 'href' in link and 'special' not in link['href']:
                links.append(link['href'])

    return links[3:]

def get_links_2020() -> list[str]:
    '''
    Returns a list of the top 100 CNN articles from 2020
    '''
    url = "https://www.cnn.com/2020/12/23/us/top-100-digital-stories-2020-trnd/index.html"
    cnn2020 = scraper.get(url)

    links = []
    for div in scraper.find_all('div', cnn2020):
        if 'class' in div and 'zn-body__paragraph' in div['class']:
            for link in scraper.find_all('a', div['element']):
                if 'href' in link and 'special' not in link['href']:
                    links.append(link['href'])

    return links[1:]

def get_article(link: str) -> str:
    '''
    Returns the text in a CNN Live/Regular Story written between 2020-2019
    '''
    article_source = scraper.get(link)
    article = []

    markers = ['dCwndB', 'paragraph', 'cnnix-article__paragraph']
    for paragraph in scraper.find_all('p', article_source):
        if 'class' in paragraph and any([marker in paragraph['class'] for marker in markers]):
            article.append(paragraph['text'])

    for div in scraper.find_all('div', article_source):
        if 'class' in div and 'zn-body__paragraph' in div['class']:
            article.append(div['text'])

    article = '\n'.join(article)
    article = ' '.join(article.split())
    return article


def run() -> str:
    data = {'2019': [], '2020': []}

    print('Reading Top CNN Articles 2019')
    links = get_links_2019()
    for i, link in enumerate(links):
        print('Retrieving article', i+1)
        article = get_article(link)
        data['2019'].append(article)

    print('Reading Top CNN Articles 2020')
    links = get_links_2020()
    for i, link in enumerate(links):
        print('Retrieving article', i+1)
        article = get_article(link)
        data['2020'].append(article)

    return data

if __name__ == '__main__':
    pass

