"""General purpose plotting module for the source class"""
from typing import Callable
import plotly.figure_factory as ff
import plotly.graph_objects as go
from source import Source
import hypothesis


def source_dist(source: Source, title: str, path: str) -> None:
    """Produces a histrogram with two cureves correseponding to 2019, 2020"""
    scores_2019, scores_2020 = source.get_scores()
    group_labels = ['2019', '2020']
    colors = ['#abd948', '#cf2950']

    fig = ff.create_distplot([scores_2019, scores_2020], group_labels, bin_size=0.8, colors=colors)
    fig.update_layout(title=title)
    fig.write_html(path)


def combined_source_dist(sources: list[Source], title: str, path: str) -> None:
    """Produces a histogram with multiple sources aarranged by year"""
    colors = ['#cf2950', '#991232', '#aaaaaa', '#000000', '#5496ff', '#0448b5']
    data = [score for source in sources for score in source.get_scores()]
    group_labels = [f'{source.name} - {year}' for source in sources for year in ['2019', '2020']]

    fig = ff.create_distplot(data, group_labels, bin_size=0.8, colors=colors, show_hist=False)
    fig.update_layout(title=title)
    fig.write_html(path)


def hypothesis_table(sources: list[Source], func: Callable[[float], float], path: str) -> None:
    """Plots a table containing the values of each source
    calculated using the function as well the p-value obtained
    using the hypothesis module
    """
    column_names = ['Source', f'{func.__name__} 2019',
                    f'{func.__name__} 2020', 'Difference', 'p value']
    data = [[] for _ in range(5)]
    for source in sources:
        data[0].append(source.name)
        scores_2019, scores_2020 = source.get_scores()
        data[1].append(round(func(scores_2019), 2))
        data[2].append(round(func(scores_2020), 2))
        p = hypothesis.p_value(source, func)
        data[3].append(round(p['test_statistic'], 2))
        data[4].append(p['p'])

    fig = go.Figure(data=[go.Table(header=dict(values=column_names),
                    cells=dict(values=data))])
    fig.write_html(path)


def sampling_distribution(source: Source, func: Callable[[float], float],
                          title: str, path: str) -> None:
    """Plots a sampling distributon using a source"""
    p = hypothesis.p_value(source, func)
    group_labels = [f'{func.__name__} Difference']

    fig = ff.create_distplot([p['sampling_distribution']], group_labels, bin_size=0.2)
    fig.update_layout(title=title)
    fig.write_html(path)


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['plotly.figure_factory', 'plotly.graph_objects',
                          'source', 'hypothesis', 'typing'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })
