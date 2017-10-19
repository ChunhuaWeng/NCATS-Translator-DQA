"""
Scrapes information from FAIRsharing.org
"""
import requests
from lxml import html
import config


def fair_scraper(url):
    """Scrapes FAIRsharing.org for some basic information.

    Scrapes FAIRsharing.org for some basic information, including title, scope and data types, terminology artifacts,
    and conditions of use.

    :param url: String url to page to scrape
    :return: FAIRPrelimStats object
    """
    # output message
    if config.verbose:
        print('Scraping: ' + url)

    # load the page
    page = requests.get(url)

    # parse the HTML
    html_content = html.fromstring(page.content)

    # Get the database name
    # <div class="title-text">
    #   <h2>
    #     <img src="https://fairsharing.org/static/img/status_circles/ready.png"  class="view_status_icon" alt="ready" data-toggle="tooltip" data-placement="bottom" title=""/>
    #     ChEMBL: a large-scale bioactivity database for drug discovery
    #   </h2>
    # </div>
    title = html_content.xpath('//div[@class="title-text"]/h2/text()[last()]')
    title = title[0].strip()

    # Find the listed items under Scope and data types
    # Example:
    # <li class="bio-tag domain">
    #     <span class="bio-icon-tag"style="padding-right: 5px"></span>
    #     Approved drug
    # </li>
    sad = html_content.xpath('//li[@class="bio-tag domain"]/text()[last()]')
    sad = [x.strip() for x in sad]

    # Find the list items under Terminology Artifacts
    # Example:
    # <p><span class="heavier">Terminology Artifacts</span></p>
    # <ul class="record-list-link">
    # 	<li class="small"><a href="/bsg-s000039" target="_blank">Chemical Entities of Biological Interest</a></li>
    # 	<li class="small"><a href="/bsg-s000136" target="_blank">PSI Molecular Interaction Controlled Vocabulary</a></li>
    # </ul>
    ta = html_content.xpath('//span[text()="Terminology Artifacts"]/../../ul/li/a/text()')
    ta = [x.strip() for x in ta]

    # Get license
    # Example:
    # <div class="standard-unit">
    # <p class="section-title"><span class="heavier">Conditions of Use</span></p>
    # <!-- ...  -->
    # <span class="section-header">
    # 	Applies to:
    #
    # 	Data use
    #
    # 	</span>
    # <ul>
    # 	<li>
    # 		<span class="small"><a href="https://creativecommons.org/licenses/by/3.0/" target="_blank">Creative Commons Attribution (CC-BY) 3.0 International</a></span>
    # 	</li>
    # </ul>
    # <span class="section-header">
    # 	Applies to:
    #
    #
    # 			Database software
    #
    #
    # 	</span>
    # <ul>
    # 	<li>
    # 		<span class="small"><a href="http://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License 2.0</a></span>
    # 	</li>
    # </ul>
    # <div class="clearfix"></div>
    # Notes: multiple groupings of data use (as shown above). Also, some license list items are not inside of links

    # Gets the license "Applies to..." grouping
    lic_groups = html_content.xpath('//span[text()="Conditions of Use"]/../../span[@class="section-header"]')
    lic_info = []

    for lic_group in lic_groups:
        # Get the "Applies to" text and fix weird whitespace
        applies_to = lic_group.xpath('text()')
        applies_to = ' '.join(applies_to[0].split())

        # Get the licenses
        licenses = lic_group.xpath('following-sibling::ul[1]/li/span//text()')
        licenses = [x.strip() for x in licenses]

        # Add the license information as a tuple
        lic_info.append((applies_to, licenses))

    return FAIRPrelimStats(url, title, sad, ta, lic_info)


class FAIRPrelimStats:
    """
    Class that contains scraped information from FAIRsharing.org

    Public members:
    title - String title of the database
    scope_and_data_types - List of strings
    terminology_artifacts - List of strings
    license - List of tuples (usage scenario, List of license strings)
    """

    def __init__(self, url='', title='', sad=[], ta=[], lic=[]):
        """FAIRPrelimStats constructor

        :param title: DB title (string)
        :param sad: Scope and data types (list of strings)
        :param ta: Terminology artifacts (list of strings)
        :param lic: List of tuples (usage scenario, List of license strings)
        """
        self.url = url
        self.title = title
        self.scope_and_data_types = sad
        self.terminology_artifacts = ta
        self.license = lic
