
# coding: utf-8

# ## FAIRSharing metrics
# 
# Write out dataset data quality metrics in RDF using W3C data vocabulary.  
# Converting preliminary statistics to W3C DQV

# In[1]:


from rdflib import Graph, Literal, URIRef, Namespace, RDF
from rdflib.namespace import DCTERMS, XSD


# In[2]:


import json


# In[3]:


#!python scrapper.py
#!conda install -c conda-forge rdflib -y
#do it once


# In[20]:


#THE SCRAPPER HAS TO BE A MODULE WHERE I CAN DEFINE THE URL EN GET THE METHOD


# In[4]:


metrics = json.loads(open('metrics.json').read())
catalog = json.loads(open('downloadURL.json').read())
details = json.loads(open('details.json').read())


# In[5]:


# Define namespaces
dqv = Namespace("http://www.w3.org/ns/dqv#")
hcls = Namespace("http://www.w3.org/hcls#")
bio2rdf = Namespace("http://bio2rdf.org#")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
prov = Namespace("https://www.w3.org/ns/prov#")
dcat = Namespace("http://www.w3.org/ns/dcat#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")


# In[6]:


g = Graph()


# In[7]:


dataset = catalog[str(metrics['url'])]
distribution = dataset + 'datasetDistribution'


# In[21]:


# THE MODULE NEEDS A CONDITION HERE TO DO EVERYTHING IF THE MEASUREMENT EXIST


# In[8]:


#metrics_names = [i for i in metrics.keys()]
#I've to make a condition to break when other metrics are not used
metrics_names = ['vocabReuse', 'license', 'coverage'] # if url or title skip
metrics_names


# In[9]:


# Add information about the data set
g.add((URIRef(dataset), rdf.type, dcat.Dataset))
g.add((URIRef(dataset), dcterms.title, Literal(metrics['title'], lang="en")))
g.add((URIRef(dataset), dcat.distribution, URIRef(distribution)))


# In[10]:


# Add information about the distribution
g.add((URIRef(distribution), rdf.type, dcat.distribution))
g.add((URIRef(distribution), dcat.downloadURL, URIRef(metrics['url'])))
g.add((URIRef(distribution), dcterms.title, Literal(metrics['title'], lang="en")))


# In[18]:


for metric in metrics_names:
    measurement = hcls+str(metric)
    measure_value = metrics[str(metric)]
    dqv_metric = dqv+details[str(metric)]['DQVmetric']
    skos_type = details[str(metric)]['SKOStype']
    dqv_dimension = dqv+details[str(metric)]['DQVdimension']
    skos_label =  details[str(metric)]['DQVdimension']
    skos_definition = details[str(metric)]['SKOSdefinition']
    dqv_category = dqv + details[str(metric)]['DQVcategory']
    # Add information about the Measurement
    g.add((URIRef(distribution), dqv.hasQualityMeasurement, URIRef(measurement)))
    g.add((URIRef(measurement), rdf.type, dqv.QualityMeasurement))
    g.add((URIRef(measurement), dqv.computedOn, URIRef(distribution)))
    g.add((URIRef(measurement), dqv.isMeasurementOf, URIRef(dqv_metric)))
    # Add information about the Metric
    g.add((URIRef(dqv_metric), rdf.type, dqv.QualityMeasurement))
    g.add((URIRef(dqv_metric), skos.type, Literal(skos_type, lang="en")))
    g.add((URIRef(dqv_metric), dqv.expectedDatatype, xsd.string))
    g.add((URIRef(dqv_metric), dqv.inDimension, URIRef(dqv_dimension)))
    # Add information about the Dimension
    g.add((URIRef(dqv_dimension), rdf.type, dqv.Dimension))
    g.add((URIRef(dqv_dimension), skos.prefLabel, Literal(skos_label, lang="en")))
    g.add((URIRef(dqv_dimension), skos.definition, Literal(skos_definition, lang="en")))
    g.add((URIRef(dqv_dimension), dqv.inCategory, URIRef(dqv_category)))
    g.add((URIRef(dqv_category), rdf.type, dqv.Category))
    for value in measure_value:
        g.add((URIRef(measurement), dqv.value, Literal(value, lang="en")))


# In[19]:


g.serialize(destination='test.ttl')


# In[30]:


#g.serialize(destination='test.html')


# In[ ]:


#reates and adds a new measurement to the graph
#:param measurement_label: A unique label for the measurement. Leave empty for auto naming.
#:return: The new measurement node
if len(measurement_label) == 0:
    # Create a new measurement label
    n_measurements += 1
    measurement_label = 'measurement' + '%04d' % n_measurements


# In[ ]:


def serialize(self, file, format='ttl'):
    """Writes the RDF graph to file in the specified format

    :param file: Path to the file to write to (String)
    :param format: RDF format (default: 'ttl')
    :return:
    """
    try:
        # Write out turtle file
        self.g.serialize(destination=file, format=format)

        # Output message
        if config.verbose:
            print('Preliminary statistics in W3C DQV written to: ' + file)
    except IOError:
        sys.stderr.write('Error while trying to serialize preliminary stats RDF graph to file: ' + file + '\n')


# ## Testing

# In[ ]:


# I NEED A CONDITION THAT SAYS THE DOWNLOAD URL IS NOT IN THE CATALOG


# In[ ]:


# FAIRsharing.org URLs to test
urls = ['https://biosharing.org/biodbcore-000015',
        'https://biosharing.org/biodbcore-000037',
        'https://biosharing.org/biodbcore-000081',
        'https://biosharing.org/biodbcore-000095',
        'https://biosharing.org/biodbcore-000104',
        'https://biosharing.org/biodbcore-000137',
        'https://biosharing.org/biodbcore-000155',
        'https://biosharing.org/biodbcore-000156',
        'https://biosharing.org/biodbcore-000173',
        'https://biosharing.org/biodbcore-000304',
        'https://biosharing.org/biodbcore-000329',
        'https://biosharing.org/biodbcore-000330',
        'https://biosharing.org/biodbcore-000341',
        'https://biosharing.org/biodbcore-000417',
        'https://biosharing.org/biodbcore-000438',
        'https://biosharing.org/biodbcore-000441',
        'https://biosharing.org/biodbcore-000455',
        'https://biosharing.org/biodbcore-000470',
        'https://biosharing.org/biodbcore-000495',
        'https://biosharing.org/biodbcore-000525',
        'https://biosharing.org/biodbcore-000544',
        'https://biosharing.org/biodbcore-000552',
        'https://biosharing.org/biodbcore-000663',
        'https://biosharing.org/biodbcore-000730',
        'https://biosharing.org/biodbcore-000805',
        'https://biosharing.org/biodbcore-000826',
        'https://biosharing.org/biodbcore-000842',
        'https://fairsharing.org/biodbcore-000618',
        'https://fairsharing.org/biodbcore-000340']

# Write the results to the configured output folder
dir_output = config.path_output
if not os.path.exists(dir_output):
    os.mkdir(dir_output)

# List of preliminary statistics results
stats_list = []

# Process each url
for url in urls:
    # Scrape the page
    stats = fair_scraper.fair_scraper(url)
    stats_list.append(stats)

    # Output filename based on url
    filename = url.split('/')[-1] + '_rdf.ttl'
    output_file = os.path.join(dir_output, filename)

    # Use the dataset title as the local identifier
    dataset_id = "".join([c for c in stats.title if c.isalnum()]) + 'Dataset'

    # Write out preliminary statistics using W3C DQV
    stats_rdf = prelim_stats_rdf.PrelimStatsRDF(dataset_id, stats)
    stats_rdf.serialize(output_file, format='ttl')

# Run the scraper and write the results to CSV
file_output = os.path.join(dir_output, 'FAIRsharing_table.csv')
#fair_scraper.fair_table(stats_list, file_output)

