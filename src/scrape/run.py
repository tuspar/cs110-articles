from scrape.sources.cnn import cnn
from scrape.sources.newyorker import newyorker

import json

def runner(source):
    data = {'2019':[], '2020':[]}
    name = source.__name__

    print(f'Reading Top {name} Articles 2019')
    links = source.get_links_2019()
    for i, link in enumerate(links):
        print('Retrieving article', i+1)
        article = source.get_article(link)
        data['2019'].append(article)

    print(f'Reading Top {name} 2020')
    links = source.get_links_2020()
    for i, link in enumerate(links):
        print('Retrieving article', i+1)
        article = source.get_article(link)
        data['2020'].append(article)
    
    for r in source.remove:
        data['2019'].pop(r)
        data['2020'].pop(r)

    with open(f'data/{name}.json', 'w') as f:
        f.write(json.dumps(data))
    
    return data


def get_data():
    sources = [cnn, newyorker]
    data = {}
    for source in sources:
        data[source.__name__] = runner(source)
    return data


if __name__ == '__main__':
    get_data()