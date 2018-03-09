
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


metrics = json.loads(open('../catalogs/metrics.json').read())
catalog = json.loads(open('../catalogs/downloadURL.json').read())
details = json.loads(open('../catalogs/details.json').read())


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


g.serialize(destination='chembl.nt', format='nt')

print('FAIRsharing Metrics Fsile Created')
