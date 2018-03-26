# Fairsharing Metrics

[![License](https://img.shields.io/badge/FAIR-metrics-orange.svg)](http://fairmetrics.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Dockerization of the Fairsharing metrics as a module for Data Quality Analysis.
The purpose of this project is to provide automation as a stand-alone implementation in order to escalate on more general data quality assessment.

## Prerequisites

- Installing [Docker](https://docs.docker.com/) for [Mac](https://docs.docker.com/docker-for-mac/install/) and [Windows](https://docs.docker.com/docker-for-windows/install/download-docker-for-windows)

![docker](img/docker.png)

## Usage

### Clone the repository

        git clone https://github.com/pedrohserrano/fairsharing-metrics.git && \
        cd fairsharing-metrics

### Build the Docker image

        docker build -t fairsharing-metrics .

### Run the Docker container to get the FAIRmetrics

        docker run -it --rm \
        -v "$PWD"/FAIRsharing:/root/FAIRsharing \
        fairsharing-metrics <URL>

    urls = ['https://fairsharing.org/biodbcore-000015',
            'https://fairsharing.org/biodbcore-000304',
            'https://fairsharing.org/biodbcore-000456',
            'https://fairsharing.org/bsg-s000909']


## Licence

The MIT License (MIT) 2017

## Acknowledgments

- [RDFUnit](http://aksw.org/Projects/RDFUnit.html)
- [FAIRsharing.org](http://FAIRsharing.org)