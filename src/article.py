"""Article Dataclass"""
from dataclasses import dataclass
import sentiment


@dataclass
class Article:
    """Article Dataclass

    Instance Attributes:
       - body: The text within the article
       - polarity: The 'happiness' of the article
    """

    body: str
    polarity: float

    def __init__(self, body: str) -> None:
        self.body = body

    def score(self, lexicon: dict[str: float]) -> None:
        """Sets a polrity score using given lexicon"""
        self.polarity = sentiment.polarity(lexicon, self.body)

    def json(self) -> dict:
        """Returns article object as json"""
        return {'body': self.body, 'polarity': self.polarity}

    @staticmethod
    def load(article_dict: dict) -> 'Article':
        """Uses a dictionary representation to make a article object"""
        article = Article(article_dict['body'])
        article.polarity = article_dict['polarity']

        return article


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['doctest', 'sentiment', 'dataclasses'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
