"""Custom web scraping implementation"""
import urllib.request
import doctest
import python_ta


def get(url):
    """
    Returns raw HTML as a string
    """
    con = urllib.request.urlopen(url)
    bhtml = con.read()
    con.close()

    return bhtml.decode("utf8") 


def find_all(tag: str, data: str) -> list:
    """
    Returns a list containing all the elements with the specified tag.
    Each element is mapped to a dictionary containing itself, all of
    it's attributes and the text contained in it and any sub-elements

    Example Usage:
    >>> html = '<html><body><h1>My First Heading</h1><p class="content">My first paragraph.</p></body></html>'
    >>> actual = find_all('p', html)
    >>> expected = [{
    ...     'element': '<p class="content">My first paragraph.</p>', 
    ...     'header': 'class="content', 
    ...     'class': 'content', 
    ...     'text': 'My first paragraph.'
    ... }]
    >>> actual == expected
    True
    """
    lst = []
    elements = text_between(data, f'<{tag} ', f'</{tag}>', inclusive=True)
    elements = [element for element in elements if element != '']

    for element in elements:
        map = {
            'element': element, 
            'header': text_between(element, f'<{tag} ', f'\">', inclusive=False)[0]
        }
        
        attributes = map['header'].split('" ')
        for attribute in attributes:
            attribute = attribute.split('="')
            if len(attribute) == 2:
                map[attribute[0]] = attribute[1]
        
        map['text'] = ''.join(text_between(element, '>', '<', inclusive=False))
        lst.append(map)

    return lst


def text_between(data: str, a: str, b: str, inclusive: bool) -> list[str]:
    """
    Returns text all instances of text between two selectors

    >>> actual = text_between('abcdefghijklmnopqrstuvwxyzde11xy', 'de', 'xy', inclusive=False)
    >>> actual == ['fghijklmnopqrstuvw', '11']
    True
    """
    indices = []
    texts = []
    
    start = 0
    data.find(a)
    while data.find(a, start) != -1:
        start = data.find(a, start) + len(a)
        indices.append(start)

    for index in indices:
        end = data.find(b, index)
        if inclusive:
            texts.append(data[index-len(a):end+len(b)])
        else:
            texts.append(data[index:end])
    
    return texts


if __name__ == '__main__':
    """
        TODO:
          - Fix Python-TA Error
    """
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['urllib.request', 'doctest'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
