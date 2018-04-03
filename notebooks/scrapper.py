
# coding: utf-8

# Fair Scraper

"""
Scrapes information from FAIRsharing.org
"""
import os
import requests
from lxml import html
import pandas as pd
import json


# #### fair_scraper(url)
# FAIRsharing.org for some basic information.
# 
#     Scrapes FAIRsharing.org for some basic information, including title, scope and data types, terminology artifacts,
#     and conditions of use.
# 
#     :param url: String url to page to scrape
#     :return: FAIRPrelimStats object

url = 'https://fairsharing.org/biodbcore-000015'
page = requests.get(url)
html_content = html.fromstring(page.content)

# - Get the title
title = html_content.xpath('//div[@class="title-text"]/h2/text()[last()]')
title = title[0].strip()
print(title)

# - Get the tags (Scope and data types)
sad = html_content.xpath('//li[@class="bio-tag domain"]/text()[last()]')
sad = [x.strip() for x in sad]
print(sad)

# - Get the terminology artifacts
ta = html_content.xpath('//span[text()="Terminology Artifacts"]/../../ul/li/a/text()')
ta = [x.strip() for x in ta]
print(ta)

# - Get the license
lic_groups = html_content.xpath('//span[text()="Conditions of Use"]/../../span[@class="section-header"]')

lic_info = []
for lic_group in lic_groups:
    applies_to = lic_group.xpath('text()') # Get the "Applies to" text and fix weird whitespace
    applies_to = ' '.join(applies_to[0].split())
    licenses = lic_group.xpath('following-sibling::ul[1]/li/span//text()')     # Get the licenses
    licenses = [x.strip() for x in licenses]
    lic_info.append((applies_to, licenses))     # Add the license information as a tuple


lic_strings = []
sep = '; '
for lic in lic_info:
    lic_strings.append(lic[0] + " = {" + sep.join(lic[1]) + "}")
    lic_string = sep.join(lic_strings)


licence = [lic_string]
print(licence)

# - FAIR Scrapper elements  
# url, title, sad, ta, lic_info

fpss = [url, title, sad, ta, licence]
num_fpss = len(fpss)

titles = ['url', 'title', 'scope and data types', 'terminology artifacts', 'license']
zip_fpss = {key: value for (key, value) in zip(titles, fpss)}


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)


writeToJSONFile('./','metrics',zip_fpss)


