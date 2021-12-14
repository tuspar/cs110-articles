import os
import dataset
import statistics
import plot

DATASET_FOLDER = 'data'
OUT_FOLDER = 'out'
P_VALUE_TESTING_REPETITIONS = 5000

for folder in [DATASET_FOLDER, OUT_FOLDER]:
    if not os.path.isdir(folder):
        os.mkdir(folder)

sources = dataset.get(DATASET_FOLDER)

plot.combined_source_dist(sources, 'Combined Polarity Distribution', f'{OUT_FOLDER}/combined_dist.html')
for source in sources:
    path = f'{OUT_FOLDER}/{source.name}_dist.html'
    title = f'Polarity Distribution: {source.name}'
    plot.source_dist(source, title, path)

for func in [statistics.mean, statistics.median]:
    plot.hypothesis_table(sources, func, f'{OUT_FOLDER}/p_values_{func.__name__}.html')
    for source in sources:
        plot.sampling_distribution(source, func, f'Sampling Distribution: {source.name}', f'{OUT_FOLDER}/{func.__name__}_sampl_dist_{source.name}.html')