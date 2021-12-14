"""Subclass of source implemented for The New Yorker"""
import scraper
from source import Source
from article import Article


class NewYorker(Source):
    """Subclass of source implemented for The New Yorker"""

    _remove: list[int] = [8, 3]

    def _get_links_by_year(self, year: str) -> list[str]:
        """..."""
        url = (f'https://www.newyorker.com/culture/{year}-in-review/'
               + f'the-top-twenty-five-new-yorker-stories-of-{year}')

        html = scraper.get(url)

        links = []
        for div in scraper.find_all('div', html):
            if 'class' in div and 'heading-h4' in div['class']:
                for link in scraper.find_all('a', div['element']):
                    links.append(link['href'])
        return links

    def _get_article(self, link: str) -> Article:
        """Returns the text in a TNY Live/Regular Story written between 2020-2019"""
        source = scraper.get(link)
        article = []

        for paragraph in scraper.find_all('p', source):
            if 'class' in paragraph and 'paywall' in paragraph['class']:
                article.append(paragraph['text'])

        return Article(' '.join(article))


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
