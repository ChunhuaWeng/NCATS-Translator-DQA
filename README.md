NCATS Translator Data Quality Analysis pipeline

This project analyzes quality statistics of datasets selected for the NCATS Translator project.

fair_tester.py scrapes information from a list of datasets specified by their FAIRsharing.org url and writes the results to a tab delimited CSV file. 

fair_rdf_tester.py scrapes information from a list of datasets specified by their FAIRsharing.org url and writes the results in RDF (turtle format) with one output file per FAIRsharing.org url. 

computational_metrics_tester.py computes computational metrics using RDFUnit, creates a W3C DQV report, and imports this report into a new GraphDB repository.

The code is written in Python3 (requires version 3.6+) and requires the following libraries:  
requests: pip install requests  
lxml: pip install lxml  
pandas: pip install pandas  
rdflib: pip install rdflib

Please make a copy of config.py.DEFAULT, rename it to config.py, and edit the configuration for your system. 