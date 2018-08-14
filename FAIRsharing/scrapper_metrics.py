import os
import sys
import requests
from lxml import html
from rdflib import Graph, Literal, URIRef, Namespace, RDF
from rdflib.namespace import DCTERMS, XSD
import time
import datetime
import json

timestarted = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

# #### fair_scraper(url)
# FAIRsharing.org for some basic information.
# 
#     Scrapes FAIRsharing.org for some basic information, including title, scope and data types, terminology artifacts,
#     and conditions of use.
# 
#     :param url: String url to page to scrape
#     :return: FAIRPrelimStats object

url = str(sys.argv [1])#'https://fairsharing.org/biodbcore-000015'
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

titles = ['url', 'title', 'coverage', 'vocabReuse', 'license']
metrics = {key: value for (key, value) in zip(titles, fpss)}


#=====================================

# ## FAIRSharing metrics
# Write out dataset data quality metrics in RDF using W3C data vocabulary.  
# Converting preliminary statistics to W3C DQV


catalog = json.loads(open('downloadURL.json').read())
details = json.loads(open('details.json').read())

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
prov = Namespace("http://www.w3.org/ns/prov#")

# Define the graph

g = Graph()
dataset = catalog[str(metrics['url'])]
distribution = dataset + 'datasetDistribution'
metrics_names = ['vocabReuse', 'license', 'coverage'] # if url or title skip

# Add information about the data set
g.add((URIRef(dataset), rdf.type, dcat.Dataset))
g.add((URIRef(dataset), dcterms.title, Literal(metrics['title'], lang="en")))
g.add((URIRef(dataset), dcat.distribution, URIRef(distribution)))
# Add information about the provenance
g.add((URIRef(dataset), prov.generated, bio2rdf.provenance))
g.add((bio2rdf.provenance, rdf.type, prov.Activity))
g.add((bio2rdf.provenance, prov.startedAtTime, Literal(str(timestarted),datatype=XSD.time)))
# Add information about the distribution
g.add((URIRef(distribution), rdf.type, dcat.distribution))
g.add((URIRef(distribution), dcat.downloadURL, URIRef(metrics['url'])))
g.add((URIRef(distribution), dcterms.title, Literal(metrics['title'], lang="en")))

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


def serialize_file(file, format='ttl'):
    """Writes the RDF graph to file in the specified format

    :param file: Path to the file to write to (String)
    :param format: RDF format (default: 'ttl')
    :return:
    """
    try:
        # Write out turtle file
        g.serialize(destination=file, format=format)
        print('FAIRsharing Metrics in W3C DQV written to: ' + file)
    except IOError:
        sys.stderr.write('Error while trying to serialize fairsharing metrics RDF graph to file: ' + file + '\n')


#format_file = sys.arg[2]

write_timestamp = '/data/fairsharing/'+str(metrics['title'][:8]) + str(timestarted) + '.nt'
serialize_file(write_timestamp, 'nt')

write = '/data/fairsharing.nt'
serialize_file(write, 'nt')
