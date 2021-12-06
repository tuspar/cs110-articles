'''
Main Dataset Management File
'''
import json
import doctest
import python_ta

from source import Source
from cnn import CNN
from newyorker import NewYorker
from guardian import Guardian


def __write_json(data: str, filepath: str) -> None:
    '''Saves data string to json at specified filepath'''
    with open(filepath, 'w') as f:
        f.write(json.dumps(data))


def __read_json(filepath: str) -> dict:
    '''Reads data string from json at specified filepath'''
    with open(filepath, 'r') as f:
        return json.loads(f.read())


def runner(source: Source) -> dict:
    '''Uses a source to retrieve the dataset required'''
    data = {'2019': [], '2020': []}
    name = source.__name__

    print(f'Reading Top {name} Articles 2019')
    links = source.get_links_2019()
    for i, link in enumerate(links):
        print('Retrieving article', i + 1)
        article = source.get_article(link)
        data['2019'].append(article)

    print(f'Reading Top {name} 2020')
    links = source.get_links_2020()
    for i, link in enumerate(links):
        print('Retrieving article', i + 1)
        article = source.get_article(link)
        data['2020'].append(article)

    for r in source.remove:
        data['2019'].pop(r)
        data['2020'].pop(r)

    __write_json(data, f'data/{name}.json')
    return data


def get_data() -> dict:
    '''Gets and saves dataset for all available sources'''
    sources = [CNN, NewYorker, Guardian]
    data = {}
    for source in sources:
        data[source.__name__] = runner(source)
    __write_json(data, 'data/data.json')
    return data


def read_data() -> dict:
    '''Reads pre-loaded data for all sources'''
    return __read_json('data/data.json')


def get_or_read() -> None:
    '''Not Implemented'''


if __name__ == '__main__':
    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['doctest', 'source', 'cnn', 'newyorker', 'guardian', 'json'],
        'allowed-io': ['__write_json', '__read_json', 'runner'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
