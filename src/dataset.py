'''
Main Dataset Management File
'''
import os
import doctest
import python_ta

from source import Source
from cnn import CNN
from newyorker import NewYorker
from guardian import Guardian
import sentiment

def get(dataset_folder):
    """Get Dataset"""
    lexicon = sentiment.get_lexicon()
    sources = [CNN(), NewYorker(), Guardian()]

    for i in range(len(sources)):
        path = f'{dataset_folder}/{sources[i].name}.json'
        if os.path.exists(path):
            sources[i] = Source.load(path)
        else:
            sources[i].get_links()
            sources[i].get_articles()
            for articles in [sources[i].articles_2019, sources[i].articles_2020]:
                for article in articles:
                    article.score(lexicon)
            sources[i].save(path)

    return sources

 
def score(source: Source, lexicon: dict[str: float]):
    for articles in [source.articles_2019, source.articles_2020]:
        for article in articles:
            article.score(lexicon)

if __name__ == '__main__':
    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['doctest', 'source', 'cnn', 'newyorker', 'guardian', 'sentiment', 'os'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
