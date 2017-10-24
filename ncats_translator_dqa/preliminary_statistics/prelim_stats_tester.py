"""Tests the fair_scraper and fair_quality_rdf functions on the databases in the NCATS Data Quality Google spreadsheet.
Outputs an RDF file (turtle .ttl format) for each dataset tested with the filename based on the FAIRsharing.org URL.
"""

import os
import csv
from ncats_translator_dqa import config
from ncats_translator_dqa.preliminary_statistics import fair_scraper, prelim_stats_rdf

# FAIRsharing.org URLs to test
urls = ['https://biosharing.org/biodbcore-000015',
        'https://biosharing.org/biodbcore-000037',
        'https://biosharing.org/biodbcore-000081',
        'https://biosharing.org/biodbcore-000095',
        'https://biosharing.org/biodbcore-000104',
        'https://biosharing.org/biodbcore-000137',
        'https://biosharing.org/biodbcore-000155',
        'https://biosharing.org/biodbcore-000156',
        'https://biosharing.org/biodbcore-000173',
        'https://biosharing.org/biodbcore-000304',
        'https://biosharing.org/biodbcore-000329',
        'https://biosharing.org/biodbcore-000330',
        'https://biosharing.org/biodbcore-000341',
        'https://biosharing.org/biodbcore-000417',
        'https://biosharing.org/biodbcore-000438',
        'https://biosharing.org/biodbcore-000441',
        'https://biosharing.org/biodbcore-000455',
        'https://biosharing.org/biodbcore-000470',
        'https://biosharing.org/biodbcore-000495',
        'https://biosharing.org/biodbcore-000525',
        'https://biosharing.org/biodbcore-000544',
        'https://biosharing.org/biodbcore-000552',
        'https://biosharing.org/biodbcore-000663',
        'https://biosharing.org/biodbcore-000730',
        'https://biosharing.org/biodbcore-000805',
        'https://biosharing.org/biodbcore-000826',
        'https://biosharing.org/biodbcore-000842',
        'https://fairsharing.org/biodbcore-000618',
        'https://fairsharing.org/biodbcore-000340']

# Write the results to the configured output folder
dir_output = config.path_output
if not os.path.exists(dir_output):
    os.mkdir(dir_output)

# List of preliminary statistics results
stats_list = []

# Process each url
for url in urls:
    # Scrape the page
    stats = fair_scraper.fair_scraper(url)
    stats_list.append(stats)

    # Output filename based on url
    filename = url.split('/')[-1] + '_rdf.ttl'
    output_file = os.path.join(dir_output, filename)

    # Use the dataset title as the local identifier
    dataset_id = "".join([c for c in stats.title if c.isalnum()]) + 'Dataset'

    # Write out preliminary statistics using W3C DQV
    stats_rdf = prelim_stats_rdf.PrelimStatsRDF(dataset_id, stats)
    stats_rdf.serialize(output_file, format='ttl')

# Run the scraper and write the results to CSV
file_output = os.path.join(dir_output, 'FAIRsharing_table.csv')
fair_scraper.fair_table(stats_list, file_output)
