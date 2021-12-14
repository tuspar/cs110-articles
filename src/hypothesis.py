"""Hypothesis Testing Module for Source objects"""
from random import shuffle
from typing import Callable
from source import Source


def p_value(source: Source, func: Callable[[float], float]) -> dict:
    """Calculates the p value of the difference of output
    between articles of 2019 and 2020 using the given function
    """
    REPETITIONS = 5000
    scores_2019, scores_2020 = source.get_scores()
    scores = scores_2019 + scores_2020
    test_statistic = func(scores_2019) - func(scores_2020)

    sampling_distribution = []
    for _ in range(REPETITIONS):
        shuffle(scores)
        mid = len(scores) // 2
        sample_statistic = func(scores[:mid]) - func(scores[mid:])
        sampling_distribution.append(sample_statistic)

    extremes = 0
    for i in sampling_distribution:
        if abs(test_statistic) <= abs(i):
            extremes += 1
    return {
        'p': extremes / REPETITIONS,
        'sampling_distribution': sampling_distribution,
        'test_statistic': test_statistic
    }


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['doctest', 'random', 'typing', 'source'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
