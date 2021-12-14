from textblob import TextBlob
import scraper

def get_lexicon():
    with open('en-sentiment.xml', 'r') as f:
        xml = f.read()
        words = scraper.__text_between(xml, 'form="', '"', inclusive=False)
        polarities = scraper.__text_between(xml, 'polarity="', '"', inclusive=False)

    lexicon = {}
    for i, word in enumerate(words):
        lexicon[word] = float(polarities[i])
    return lexicon


def _clean(text):
    """ Remove hyperlinks and markup """
    PUNCTUATION = '!\"#$%&()*+,-./:;<=>?@[]^_`{|}~'
    for p in PUNCTUATION:
        text = text.replace(p, '')

    text = text.lower()

    return text.split()


def _count_keywords(lexicon: dict[str: float], word_list: list[str]) -> dict[str, int]:
    """Return a frequency mapping of the Lexicon keywords in text.
    """
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


def polarity(lexicon: dict[str: float], text: str):
    words = _clean(text)
    occurences = _count_keywords(lexicon, words)
    polarity = _calculate_average_intensity(lexicon, occurences)

    return polarity * 100


def text_blob(lexicon, text):
    return TextBlob(text).sentiment.polarity * 100
