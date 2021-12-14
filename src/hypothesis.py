from source import Source
from random import shuffle

def p_value(source: Source, func) -> dict:
    REPETITIONS = 5000
    scores_2019, scores_2020 = source.get_scores()
    scores = scores_2019 + scores_2020
    test_statistic = func(scores_2019) - func(scores_2020)

    sampling_distribution = []
    for _ in range(REPETITIONS):
        shuffle(scores)
        mid = len(scores)//2
        sample_statistic = func(scores[:mid]) - func(scores[mid:])
        sampling_distribution.append(sample_statistic)

    extremes = 0
    for i in sampling_distribution:
        if abs(test_statistic) <= abs(i):
            extremes += 1
    return {
        'p': extremes/REPETITIONS, 
        'sampling_distribution': sampling_distribution,
        'test_statistic': test_statistic
    }

