"""Article Dataclass"""
from dataclasses import dataclass
import sentiment

@dataclass
class Article:
    """Article Dataclass"""

    body: str
    polarity: float


    def __init__(self, body):
        self.body = body


    def score(self, lexicon):
        self.polarity = sentiment.polarity(lexicon, self.body)


    def json(self) -> dict:
        return {'body': self.body, 'polarity': self.polarity}

    @staticmethod
    def load(article_dict) -> 'Article':
        article = Article(article_dict['body'])
        article.polarity = article_dict['polarity']

        return article

    