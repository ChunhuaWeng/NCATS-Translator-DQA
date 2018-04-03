'''Tests the computational_metrics function by running it with multiple datasets

Please update config.py prior to using this function.
'''

from ncats_translator_dqa.computational_metrics.computational_metrics import computational_metrics

# Absolute paths to datasets
dataset_files = [
    '/root/NCATS-Translator-DQA/Input/chembl_18.0_cellline.ttl',
    '/root/NCATS-Translator-DQA/Input/kegg-drug.ttl',
    '/root/NCATS-Translator-DQA/Input/animalqtldb.ttl'
]

# Run computational metrics on each dataset
for dataset_file in dataset_files:
    print(dataset_file)
    computational_metrics(dataset_file)
    print('\n\n')
