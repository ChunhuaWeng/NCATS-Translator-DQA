from os.path import split, join

# Get the path where the ncats_translator_dqa package resides
# This should not be changed
__local_path = split(__file__)[0]

'''Make changes to the following as necessary
'''

# Absolute path to the main RDFUnit folder
# default: 'RDFUnit' folder at the same level as 'NCATS-Translator-DQA' repository
#path_rdfunit = join(__local_path, '..', '..', 'RDFUnit')
path_rdfunit = '/root/RDFUnit/'

# URL for GraphDB
# default: 'http://localhost:7200/'
url_graphdb = 'http://localhost:7200/'

# Absolute path to output folder for preliminary statistics
# default: 'Output' folder at the same level as 'NCATS-Translator-DQA' repository
#path_output = join(__local_path, '..', 'Output')
path_output = '/root/NCATS-Translator-DQA/Output/'

# Path to resources folder
# default: resource folder under ncats_translator_dqa package
resource_path = join(__local_path, 'resources')

# Display output messages
verbose = True

