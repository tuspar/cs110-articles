'''Abstract Class for a news source that can be scraped'''
import doctest
import python_ta


class Source:
    '''Abstract Class for a news source that can be scraped'''

    remove: list[int] = []

    @staticmethod
    def get_links_2019() -> list[str]:
        '''Return list of the top Source articles of 2019'''
        raise NotImplementedError

    @staticmethod
    def get_links_2020() -> list[str]:
        '''Return list of the top Source articles of 2020'''
        raise NotImplementedError

    @staticmethod
    def get_article(link: str) -> str:
        '''Returns the text in the article provided in the link'''
        raise NotImplementedError


if __name__ == '__main__':
    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['doctest'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
