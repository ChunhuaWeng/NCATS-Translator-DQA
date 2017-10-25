# NCATS Translator Data Quality Analysis

This project analyzes quality statistics of datasets selected for the NCATS Translator project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### Python 3.6

NCATS Translator DQA is written in Python3 (requires version 3.6+). Install python3.6:

```
sudo apt install python3
```

NCATS Translator DQA requires the following libraries: requests, lxml, pandas, and rdflib.

```
sudo pip3 install requests lxml pandas rdflib
```

#### Install RDFUnit

Clone the repository:

```
git clone https://github.com/AKSW/RDFUnit.git
```

or download the latest release from [https://github.com/AKSW/RDFUnit/releases](https://github.com/AKSW/RDFUnit/releases)  

Note: The NCATS Translator DQA looks for RDFUnit in the same folder as the NCATS-Translator-DQA repository. If RDFUnit is installed to a different location, it can be specified in the DQA's configuration file (config.py)

Install JDK8 if it has not been installed yet. Maven requires the JDK but does not work with JDK9. Use JDK8 instead.  
```
sudo apt-get install openjdk-8-jdk-headless  
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-<ARCHITECTURE>/  
export PATH=$PATH:$JAVA_HOME/bin
```

Install Maven  
```
sudo apt install maven
```

Running RDFUnit for the first time should automatically build it:  
```
cd RDFUnit  
./bin/rdfunit -h
```

Note: rdfunit must be run from the RDFUnit folder, i.e., it fails when run from inside the bin folder or anywhere other than the RDFUnit folder.

#### Install GraphDB

Download GraphDB Free as a stand-alone server: [https://ontotext.com/products/graphdb/](https://ontotext.com/products/graphdb/)

Extract the downloaded zip file to a location of your choice.

Start GraphDB:  
```
./<GraphDB>/bin/graphdb
```

Open GraphDB in your browser to check that it is running. Default: http://localhost:7200

For additional information, check the [GraphDB quick start guide](http://graphdb.ontotext.com/documentation/free/quick-start-guide.html#run-graphdb-as-a-stand-alone-server)

### Installing NCATS Translator DQA

Clone the repository:  
```
git clone https://github.com/ChunhuaWeng/NCATS-Translator-DQA.git
```

Make a copy of config.py.DEFAULT, rename it to config.py, and edit the configuration for your system if needed. The path\_rdfunit may need to be editted if RDFUnit was not installed in the same location as NCATS-Translator-DQA repository. Most other settings should not need to be changed.  
```
cd NCATS-Translator-DQA/ncats_translator_dqa/  
cp config.py.DEFAULT config.py
```

Add the NCATS-Translator-DQA folder to PYTHONPATH.  
```
export PYTHONPATH=$PYTHONPATH:/path/to/the/folder/NCATS-Translator-DQA
```
Note: this must either be performed each time a terminal is opened or you can add this line to your shell's initiation script, e.g., ~/.bashrc

## Running 

translator\_dqa.py is the main tool for performing data quality analysis and can be invoked from the command line. Display help arguments for the translator\_dqa command line interface:

```
cd <NCATS-Translator-DQA>/ncats_translator_dqa
python3 translator_dqa.py -h
```

translator\_dqa can be run in one of two modes: 1) single data set; 2) multiple data sets.

### Single data set

Specify the optional arguments to collect preliminary statistics from FAIRsharing.org and/or calculate computational metrics on a data set. The path to the data file must be specified as an absolute path. 

```
python3 translator_dqa.py -f https://biosharing.org/biodbcore-000015 
python3 translator_dqa.py -d /media/casey/Data/Research/NCATS-DQ/Data/chembl_18.0_cellline.ttl
python3 translator_dqa.py -f https://biosharing.org/biodbcore-000015 -d /media/casey/Data/Research/NCATS-DQ/Data/chembl_18.0_cellline.ttl
```

The default output directory for results files is under <NCATS-Translator-DQA>/output. 

Preliminary statistics from FAIRsharing.org are saved in a tab-separated CSV file (*.csv) and as RDF in turtle format (*.ttl) conforming to the W3C Data Quality Vocabulary. The results files are named based on the URL, e.g., https://biosharing.org/biodbcore-000015 results in biodbcore-000015.csv and biodbcore-000015.ttl

Computational metrics are saved in HTML (*.html) and as RDF in turtle format (*.ttl). Computational metrics are also uploaded to GraphDB to facilitate visualization and querying in a new repository named similarly to the data filename. For example, performing computational metrics on data\_file.ext produces data\_file\_computational\_metrics.html, data\_file\_computational\_metrics.ttl, and a GraphDB repository named data\_file\_ext.

### Multiple data sets

To analyze multiple data sets, specify the FAIRsharing.org URLs and absolute paths to the data files in a N x 2 CSV file where N is the number of data sets to analyze. See <NCATS-Translator-DQA>/ncats\_translator\_dqa/resources/example\_datasets.csv for an example. 

```
python3 translator_dqa.py -m /path/to/datasets.csv
```

This will gather preliminary statistics and calculate computational metrics on the specified data sets and produce results similar as if performed on a single data set, except the preliminary statistics CSV file will combine results from all data sets. The CSV file will be named prelim\_stats\_<timestamp>.csv. 

## Troubleshooting

### Python 3.6

On Ubuntu 16.04 and below, the default Python3 version is 3.5.x. To install Python 3.6:

```
sudo add-apt-repository ppa:jonathonf/python-3.6  
sudo apt install python3.6  
wget https://bootstrap.pypa.io/get-pip.py  
sudo python3.6 get-pip.py
```

Use ```python3.6``` to invoke python and ```pip3.6``` to install required packages

### ModuleNotFoundError: No module named 'ncats_translator_dqa'

Add the NCATS-Translator-DQA folder to the PYTHONPATH environment variable. For example, if the NCATS-Translator-DQA folder exists at /home/username/NCATS-Translator-DQA:

```
export PYTHONPATH=$PYTHONPATH:/home/username/NCATS-Translator-DQA
```

You can also verify that the PYTHONPATH environment variable is set correctly:

```
echo $PYTHONPATH
python3
>>> import sys
>>> sys.path
```

### ImportError: cannot import name 'etree'

If running translator\_dqa.py produces the above error, try un-installing and re-installing lxml:

```
sudo pip3 uninstall lxml  
sudo pip3 install lxml
```

### ConnectionRefusedError:[Errno 61] Connection refused

If you see a ConnectionRefusedError after the message "GraphDB: deleting repository ...", check that GraphDB is running and that config.py has the correct URL to communicate with GraphDB. 

### GraphDB repositories are empty

translator_dqa.py initiates uploads of data files to GraphDB, but does not wait for the uploads to finish. Depending on the sizes of the validation files, it may take some time for the files to finish uploading and for GraphDB to process the new data. The new repositories for each data set should be available immediately. 

### log4j:WARN

If you see warning messages when running dqv-report like _log4j:WARN Please initialize the log4j system properly._, make a copy of the log4j.properties file  
from: <RDFUnit>/rdfunit-validate/target/classes/log4j.properties  
to: <RDFUnit>/rdfunit-w3c-dqv/target/classes/log4j.properties  
```
cd <RDFUnit>
cp rdfunit-validate/target/classes/log4j.properties rdfunit-w3c-dqv/target/classes
```

## Acknowledgments

* [RDFUnit](http://aksw.org/Projects/RDFUnit.html)
* [FAIRsharing.org](http://FAIRsharing.org)
