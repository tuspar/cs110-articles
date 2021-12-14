"""Subclass of source implemented for CNN"""
import scraper
from source import Source
from article import Article


class CNN(Source):
    """Subclass of source implemented for CNN"""

    _remove: list[int] = [39, 33, 29, 25, 8, 6, 5]

    def _get_links_by_year(self, year: str) -> list[str]:
        """..."""
        if year == '2019':
            return _get_links_2019()
        else:
            return _get_links_2020()

    def _get_article(self, link: str) -> Article:
        """..."""
        article_source = scraper.get(link)
        article = []

        markers = ['dCwndB', 'paragraph', 'cnnix-article__paragraph']
        for paragraph in scraper.find_all('p', article_source):
            if 'class' in paragraph and any(marker in paragraph['class'] for marker in markers):
                article.append(paragraph['text'])

        for div in scraper.find_all('div', article_source):
            if 'class' in div and 'zn-body__paragraph' in div['class']:
                article.append(div['text'])

        article = '\n'.join(article)
        article = ' '.join(article.split())
        return Article(article)


def _get_links_2019() -> list[str]:
    """Returns list of the top Source articles of 2019"""
    url = "https://www.cnn.com/2019/12/22/us/top-100-digital-stories-2019-trnd/index.html"
    html = scraper.get(url)
    links = []
    for paragraph in scraper.find_all('p', html):
        for link in scraper.find_all('a', paragraph['element']):
            if 'href' in link and 'special' not in link['href']:
                links.append(link['href'])

    return links[3:]


def _get_links_2020() -> list[str]:
    """Returns list of the top Source articles of 2020"""
    url = "https://www.cnn.com/2020/12/23/us/top-100-digital-stories-2020-trnd/index.html"
    html = scraper.get(url)

    links = []
    divs = []
    for div in scraper.find_all('div', html):
        if 'class' in div and 'zn-body__paragraph' in div['class']:
            divs.append(div)

    for div in divs:
        for link in scraper.find_all('a', div['element']):
            if 'href' in link and 'special' not in link['href']:
                links.append(link['href'])

    return links[1:]


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['doctest', 'scraper', 'source', 'article'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
