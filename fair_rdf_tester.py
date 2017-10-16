"""Tests the fair_scraper function on the databases in the NCATS Data Quality
# Google spreadsheet. Outputs the results in a tab-delimited CSV.
"""

import fair_scraper
import data_quality_rdf

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
urls = ['https://fairsharing.org/biodbcore-000525']

# Output file name
output_file = 'FAIR_RDF_test.ttl'

# Process each url
num_urls = len(urls)
for i in range(num_urls):
    # Scrape the page
    url = urls[i]
    stats = fair_scraper.fair_scraper(url)

    data_quality_rdf.data_quality_rdf(output_file, stats, 'http://www.fakedownload.com', 8315.7)
    # fakeFPS = fair_scraper.FAIRPrelimStats('www.FAIRshearing.org/fakeurl', 'Fake Title', ['FS1', 'FS2', 'FS3'], ['FT1', 'FT2'], [('usage', ['condition1', 'condition2'])])
    # data_quality_rdf.data_quality_rdf(output_file, fakeFPS, 'www.fakedownload.com', 8315.7)
