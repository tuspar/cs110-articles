"""Abstract Class for a news source"""
import json
from article import Article


class Source:
    """Abstract Class for a news source that can be scraped including json
    serialization and loading

    Instance Attributes:
       - name: Name of the media
       - links_2019: List containing all the links from 2019
       - articles_2019: List containing all the article objects parsed in 2019
       - links_2020: List containing all the links from 2020
       - articles_2019: List containing all the article objects parsed in 2020
       - _remove: Articles to be removed
    """

    name: str
    links_2019: list[str]
    articles_2019: list[Article]
    links_2020: list[str]
    articles_2020: list[Article]
    _remove: list[int]

    def __init__(self) -> None:
        self.name = self.__class__.__name__

    def get_links(self) -> tuple[list[str], list[str]]:
        """Sets and returns all 2019 and 2020 articles"""

        print(f'{self.name}: Retrieving 2019 Links')
        self.links_2019 = self._get_links_by_year('2019')
        print(f'{self.name}: Retrieving 2020 Links')
        self.links_2020 = self._get_links_by_year('2020')

        return self.links_2019, self.links_2020

    def _get_links_by_year(self, year: str) -> list[str]:
        """
        Returns all source links from given year

        Preconditions:
            - year in ['2019', '2020']
        """
        raise NotImplementedError

    def _get_article(self, link: str) -> Article:
        """Returns the text in the article provided in the link"""
        raise NotImplementedError

    def get_articles(self) -> tuple[list[Article], list[Article]]:
        """Gets all the articles from existing links"""
        self.articles_2019 = []
        self.articles_2020 = []
        link_article_pairs = [('2019', self.links_2019, self.articles_2019),
                              ('2020', self.links_2020, self.articles_2020)]

        for year, links, articles in link_article_pairs:
            for i, link in enumerate(links):
                if i not in self._remove:
                    print(f'{self.name}: Retrieving article {i + 1}, {year}')
                    articles.append(self._get_article(link))

        return self.articles_2019, self.articles_2019

    def save(self, path: str) -> str:
        """Serializes itself as json file and saves to path"""
        source_dict = {
            'name': self.name,
            'links_2019': self.links_2019,
            'links_2020': self.links_2020,
            'articles_2019': [article.json() for article in self.articles_2019],
            'articles_2020': [article.json() for article in self.articles_2020]
        }
        with open(path, 'w') as file:
            file.write(json.dumps(source_dict))

    @staticmethod
    def load(path: str) -> 'Source':
        """Loads source object from serialized json file"""
        with open(path, 'r') as file:
            source_dict = json.load(file)

        source = Source()
        source.name = source_dict['name']
        source.links_2019 = source_dict['links_2019']
        source.links_2020 = source_dict['links_2020']
        source.articles_2019 = [Article.load(article) for article in source_dict['articles_2019']]
        source.articles_2020 = [Article.load(article) for article in source_dict['articles_2020']]

        return source

    def get_scores(self) -> tuple[list[float], list[float]]:
        """Returns 2019, 2020 polarity scores as tuple"""
        return ([article.polarity for article in self.articles_2019],
                [article.polarity for article in self.articles_2020])


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['json', 'article'],
        'allowed-io': ['save', 'load', 'get_articles', 'get_links'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
