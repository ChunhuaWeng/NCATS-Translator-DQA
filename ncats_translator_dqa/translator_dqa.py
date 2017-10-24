import os
import argparse
import csv
from datetime import datetime
from ncats_translator_dqa import config
from ncats_translator_dqa.preliminary_statistics import fair_scraper, prelim_stats_rdf
from ncats_translator_dqa.computational_metrics.computational_metrics import computational_metrics


def translator_dqa(fair_url=None, file_data=None, file_multi=None):
    """Implementation of the command line interface for NCATS Translator Data Quality Analysis Pipeline

    :param fair_url: FAIRsharing.org url
    :param file_data: Absolute path to data file for computational metrics
    :param file_multi: Path to CSV file listing FAIRsharing.org url and data set path for each data set to test
    :return:
    """
    dir_output = config.path_output
    if not os.path.exists(dir_output):
        os.mkdir(dir_output)

    # CSV file option
    if file_multi is not None:
        # Maintain a list of preliminary stats
        prelim_stats_list = []

        # Process the CSV file line by line
        with open(file_multi) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if len(row) == 2:
                    # Preliminary statistics
                    url = row[0]
                    if url is not None:
                        url = url.strip()
                        if len(url) > 0:
                            stats = __prelim_stats(url, dir_output, False)
                            prelim_stats_list.append(stats)

                    # Computational metrics
                    file_data = row[1]
                    if file_data is not None:
                        file_data = file_data.strip()
                        if os.path.exists(file_data):
                            computational_metrics(file_data)

        # Write all preliminary statistics to a single csv
        filename = 'prelim_stats_' + datetime.now().isoformat(timespec='seconds') + '.csv'
        output_csv_file = os.path.join(dir_output, filename)
        fair_scraper.fair_table(prelim_stats_list, output_csv_file)

        # Don't process any other command line arguments
        return

    # FAIRsharing.org option
    if fair_url is not None:
        __prelim_stats(fair_url, dir_output, True)

    # Data file option
    if file_data is not None:
        computational_metrics(file_data)


def __prelim_stats(url, dir_output, write_csv=False):
    # Scrape the page
    stats = fair_scraper.fair_scraper(url)

    # Output filename based on url
    filename = url.split('/')[-1]
    output_file = os.path.join(dir_output, filename + '_rdf.ttl')

    # Use the dataset title as the local identifier
    dataset_id = "".join([c for c in stats.title if c.isalnum()]) + 'Dataset'

    # Write out preliminary statistics using W3C DQV
    stats_rdf = prelim_stats_rdf.PrelimStatsRDF(dataset_id, stats)
    stats_rdf.serialize(output_file, format='ttl')

    if write_csv:
        # Write out preliminary statistics as CSV also
        output_csv_file = os.path.join(dir_output, filename + '.csv')
        fair_scraper.fair_table([stats], output_csv_file)

    return stats

def main():
    """Defines the command line arguments and help documentation

    :return:
    """
    # Parse arguments
    parser = argparse.ArgumentParser(description=('NCATS translator data quality analysis. Gathers preliminary data '
                                                  'quality statistics and/or computational metrics on data sets.'),
                                     epilog=('Examples: \n\n'                                     
                                             'Single data set, preliminary statistics only:\n'
                                             'python3 translator_dqa.py -f https://fairsharing.org/biodbcore-000340\n\n'                                     
                                             'Single data set, computational metrics only:\n'
                                             'python3 translator_dqa.py -d /home/user/data/data.ttl\n\n'                                     
                                             'Single data set, preliminary and computational metrics:\n'
                                             'python3 translator_dqa.py -f https://fairsharing.org/biodbcore-000340 -d /home/user/data/data.ttl\n\n'                                     
                                             'Multiple data sets defined in a CSV file\n'
                                             'python3 translator_dqa.py -m /home/user/data/multiple_data_sets.csv'),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', dest='fair_url', help='FAIRsharing.org URL for preliminary statistics')
    parser.add_argument('-d', dest='file_data', help='Absolute path to data file for computational metrics')
    parser.add_argument('-m', dest='file_multi', help=('CSV file defining multiple data sets to test. Define one data '
                                                       'set on each line with format [FAIRsharing.org URL], [data set '
                                                       'file] (without brackets). Each argument is optional. If this '
                                                       'argument is used, -f and -d arguments are ignored.'))
    args = parser.parse_args()
    translator_dqa(args.fair_url, args.file_data, args.file_multi)


if __name__ == '__main__':
    main()
