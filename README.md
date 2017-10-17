NCATS Translator Data Quality Analysis pipeline

This project analyzes quality statistics of datasets selected for the NCATS Translator project.

fair_tester.py scrapes information from a list of datasets specified by their FAIRsharing.org url and writes the results to a tab delimited CSV file. 

fair_rdf_tester.py scrapes information from a list of datasets specified by their FAIRsharing.org url and writes the results in RDF (turtle format) with one output file per FAIRsharing.org url. 

The code is written in Python3 and requires the following libraries:  
requests: pip install requests  
lxml: pip install lxml  
pandas: pip install pandas  
rdflib: pip install rdflib