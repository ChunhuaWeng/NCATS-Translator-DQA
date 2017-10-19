'''Tests the computational_metrics function by running it with multiple datasets

Please update config.py prior to using this function.
'''

from computational_metrics import computational_metrics

# Absolute paths to datasets
dataset_files = [
    '/media/casey/Data/Research/NCATS-DQ/Data/chembl_18.0_cellline.ttl',
    '/media/casey/Data/Research/NCATS-DQ/Data/kegg-drug.ttl',
    '/media/casey/Data/Research/NCATS-DQ/Data/sider_effects.ttl'
]

# Run computational metrics on each dataset
for dataset_file in dataset_files:
    print(dataset_file)
    computational_metrics(dataset_file)
    print('\n\n')
