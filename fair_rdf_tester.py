"""Tests the fair_scraper and fair_quality_rdf functions on the databases in the NCATS Data Quality Google spreadsheet.
Outputs an RDF file (turtle .ttl format) for each dataset tested with the filename based on the FAIRsharing.org URL.
"""

import os
import fair_scraper
import data_quality_rdf
import config

# FAIRsharing.org URLs to test
# urls = ['https://biosharing.org/biodbcore-000015',
#         'https://biosharing.org/biodbcore-000037',
#         'https://biosharing.org/biodbcore-000081',
#         'https://biosharing.org/biodbcore-000095',
#         'https://biosharing.org/biodbcore-000104',
#         'https://biosharing.org/biodbcore-000137',
#         'https://biosharing.org/biodbcore-000155',
#         'https://biosharing.org/biodbcore-000156',
#         'https://biosharing.org/biodbcore-000173',
#         'https://biosharing.org/biodbcore-000304',
#         'https://biosharing.org/biodbcore-000329',
#         'https://biosharing.org/biodbcore-000330',
#         'https://biosharing.org/biodbcore-000341',
#         'https://biosharing.org/biodbcore-000417',
#         'https://biosharing.org/biodbcore-000438',
#         'https://biosharing.org/biodbcore-000441',
#         'https://biosharing.org/biodbcore-000455',
#         'https://biosharing.org/biodbcore-000470',
#         'https://biosharing.org/biodbcore-000495',
#         'https://biosharing.org/biodbcore-000525',
#         'https://biosharing.org/biodbcore-000544',
#         'https://biosharing.org/biodbcore-000552',
#         'https://biosharing.org/biodbcore-000663',
#         'https://biosharing.org/biodbcore-000730',
#         'https://biosharing.org/biodbcore-000805',
#         'https://biosharing.org/biodbcore-000826',
#         'https://biosharing.org/biodbcore-000842',
#         'https://fairsharing.org/biodbcore-000618',
#         'https://fairsharing.org/biodbcore-000340']

# Pages with a couple of tricky licenses for testing
urls = ['https://fairsharing.org/biodbcore-000525',
        'https://fairsharing.org/biodbcore-000155']

# Write the results to an output folder where the code resides
dir_output = config.path_prelim_stats_output
if not os.path.exists(dir_output):
    os.mkdir(dir_output)

# Process each url
for url in urls:
    # Scrape the page
    stats = fair_scraper.fair_scraper(url)

    # Output filename based on url
    filename = url.split('/')[-1] + '_rdf.ttl'
    output_file = os.path.join(dir_output, filename)

    # Write out preliminary statistics using W3C DQV
    data_quality_rdf.data_quality_rdf(output_file, stats)

