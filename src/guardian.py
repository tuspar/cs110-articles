"""Subclass of source implemented for The Guardian"""
import scraper
from source import Source
from article import Article


class Guardian(Source):
    """Subclass of source implemented for The Guardian"""

    _remove: list[int] = []

    def _get_links_by_year(self, year: str) -> list[str]:
        """..."""
        if year == '2019':
            url = "https://www.theguardian.com/news/2019/dec/24/the-best-of-the-long-read-in-2019"
        else:
            url = "https://www.theguardian.com/news/2020/dec/22/the-best-of-the-long-read-in-2020"

        source = scraper.get(url)

        links = []
        for heading_2 in scraper.find_all('h2', source):
            for link in scraper.find_all('a', heading_2['element']):
                if 'href' in link:
                    links.append(link['href'])
        return links

    def _get_article(self, link: str) -> Article:
        """Returns the text in the article provided in the link"""
        source = scraper.get(link)

        article = []
        marker = 'no-marker'
        for div in scraper.find_all('div', source):
            if 'class' in div and 'article-body-commercial-selector' in div['class']:
                paragraphs = scraper.find_all('p', div['element'])
                marker = paragraphs[0]['class']

        for paragraph in scraper.find_all('p', source):
            if 'class' in paragraph and marker in paragraph['class']:
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
