"""Main Dataset Management File"""
import os

from source import Source
from cnn import CNN
from newyorker import NewYorker
from guardian import Guardian
import sentiment


def get(dataset_folder: str, lexicon_path: str) -> list[Source]:
    """Downloads and parses dataset from the internet
    if local copy not available.
    """
    lexicon = sentiment.get_lexicon(lexicon_path)
    sources = [CNN(), NewYorker(), Guardian()]

    for i in range(len(sources)):
        path = f'{dataset_folder}/{sources[i].name}.json'
        if os.path.exists(path):
            sources[i] = Source.load(path)
        else:
            sources[i].get_links()
            sources[i].get_articles()
            score(sources[i], lexicon)
            sources[i].save(path)

    return sources


def score(source: Source, lexicon: dict[str: float]) -> None:
    """Scores all articles in the source object using given lexicon"""
    for articles in [source.articles_2019, source.articles_2020]:
        for article in articles:
            article.score(lexicon)


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['doctest', 'source', 'cnn', 'newyorker', 'guardian', 'sentiment', 'os'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
