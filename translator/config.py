from os.path import split, join

# Get the path where the ncats_translator_dqa package resides
# This should not be changed
__local_path = split(__file__)[0]

'''Make changes to the following as necessary
'''

# Absolute path to the main RDFUnit folder
path_rdfunit = '/root/RDFUnit/'

# URL for GraphDB
url_graphdb = 'http://localhost:7200/'

# Absolute path to output folder for preliminary statistics
path_output = '/root/data-quality-NCATS-translator/output/'

# Path to resources folder
# default: resource folder under ncats_translator_dqa package
resource_path = join(__local_path, 'data')

# Display output messages
verbose = True

