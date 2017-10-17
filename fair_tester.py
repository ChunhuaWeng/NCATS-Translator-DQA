"""Tests the fair_scraper function on the databases in the NCATS Data Quality
Google spreadsheet. Outputs the results in a tab-delimited CSV.
"""

import sys
import os
import pandas as pd
import fair_scraper

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

# Separate items in a list with a semicolon
sep_list = '; '

# Store results in data frame
num_urls = len(urls)
df = pd.DataFrame(index=range(0, num_urls),
                  columns=['URL', 'title', 'scope and data types', 'terminology artifacts', 'license'])

for i in range(num_urls):
    # Scrape the page
    url = urls[i]
    stats = fair_scraper.fair_scraper(url)

    # Form a string describing the licenses
    lic_strings = []
    for lic in stats.license:
        lic_strings.append(lic[0] + " = {" + sep_list.join(lic[1]) + "}")
    lic_string = sep_list.join(lic_strings)

    # Add to the data frame
    df.loc[i] = [url,
                 stats.title,
                 sep_list.join(stats.scope_and_data_types),
                 sep_list.join(stats.terminology_artifacts),
                 lic_string]

# Write the results to an output folder where the code resides
dir_code = sys.path[0]
dir_output = os.path.join(dir_code, 'output')
if not os.path.exists(dir_output):
    os.mkdir(dir_output)
output_file = os.path.join(dir_output, 'FAIRsharing_test.csv')

# Output the results as a CSV delimited with tabs
df.to_csv(output_file, sep='\t')

