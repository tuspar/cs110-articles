"""Sentiment Analysis Module"""
import scraper


def get_lexicon(path: str) -> dict[str: float]:
    """Parsers xml lexicon into a dictionary. Key is the word and value is the polarity"""
    with open(path, 'r') as f:
        xml = f.read()
        words = scraper.text_between(xml, 'form="', '"', inclusive=False)
        polarities = scraper.text_between(xml, 'polarity="', '"', inclusive=False)

    lexicon = {}
    for i, word in enumerate(words):
        lexicon[word] = float(polarities[i])
    return lexicon


def _clean(text: str) -> str:
    """Remove hyperlinks and markup """
    PUNCTUATION = '!\"#$%&()*+,-./:;<=>?@[]^_`{|}~'
    for p in PUNCTUATION:
        text = text.replace(p, '')

    text = text.lower()

    return text.split()


def _count_keywords(lexicon: dict[str: float], word_list: list[str]) -> dict[str, int]:
    """Return a frequency mapping of the Lexicon keywords in text."""
    occurrences_so_far = {}

    for word in word_list:
        if word in lexicon:
            if word not in occurrences_so_far:
                occurrences_so_far[word] = 0
            occurrences_so_far[word] += 1

    return occurrences_so_far


def _calculate_average_intensity(lexicon: dict[str: float], occurrences: dict[str, int]) -> float:
    """Return the average intensity of the given keyword occurrences.

    Preconditions:
        - occurrences != {}
        - all({occurrences[keyword] >= 1 for keyword in occurrences})
    """
    num_keywords = sum([occurrences[word] for word in occurrences])
    total_intensity = sum([lexicon[word] * occurrences[word] for word in occurrences])

    if num_keywords == 0:
        return 0
    else:
        return total_intensity / num_keywords


def polarity(lexicon: dict[str: float], text: str) -> float:
    """Return the polarity of a given string"""
    words = _clean(text)
    occurences = _count_keywords(lexicon, words)
    polarity_value = _calculate_average_intensity(lexicon, occurences)

    return polarity_value * 100


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['scraper'],
        'allowed-io': ['get_lexicon'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
