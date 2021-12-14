import doctest
import json
import python_ta
from article import Article


class Source:
    '''Abstract Class for a news source that can be scraped'''

    name: str

    def __init__(self):
        self.name = self.__class__.__name__


    def get_links(self) -> tuple[list[str], list[str]]:
        '''Sets and returns all 2019 and 2020 articles'''

        print(f'{self.name}: Retrieving 2019 Links')
        self.links_2019 = self._get_links_by_year('2019')
        print(f'{self.name}: Retrieving 2020 Links')
        self.links_2020 = self._get_links_by_year('2020')

        return self.links_2019, self.links_2020


    def _get_links_by_year(self, year) -> list[str]:
        '''
        Returns all source links from given year
        
        Preconditions:
          - url in ['2019', '2020']
        '''
        raise NotImplementedError


    def get_article(self, link: str) -> Article:
        '''Returns the text in the article provided in the link'''
        raise NotImplementedError


    def get_articles(self)-> tuple[list[Article], list[Article]]:
        '''Gets all the articles from existing links'''
        link_article_pairs = [('2019', self.links_2019, self.articles_2019), 
            ('2020', self.links_2020, self.articles_2020)]

        for year, links, articles in link_article_pairs:
            for i, link in enumerate(links):
                if not (i in self._remove):
                    print(f'{self.name}: Retrieving article {i + 1}, {year}')
                    articles.append(self._get_article(link))
    
        return self.articles_2019, self.articles_2019


    def save(self, path: str) -> str:
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
    def load(path) -> 'Source':
        with open(path, 'r') as file:
            source_dict = json.load(file)

        source = Source()
        source.name = source_dict['name']
        source.links_2019 = source_dict['links_2019']
        source.links_2020 = source_dict['links_2020']
        source.articles_2019 = [Article.load(article) for article in source_dict['articles_2019']]
        source.articles_2020 = [Article.load(article) for article in source_dict['articles_2020']]

        return source


    def get_scores(self):
        return ([article.polarity for article in self.articles_2019], 
            [article.polarity for article in self.articles_2020])