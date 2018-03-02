# Fairsharing Metrics
[![License](https://img.shields.io/badge/FAIR-metrics-orange.svg)](http://fairmetrics.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Dockerization of the Fairsharing metrics as a module for Data Quality Analysis.   
The purpose of this project is to provide automation as a stand-alone implementation in order to escalate on more general data quality assessment.

## Prerequisites

- Installing [Docker](https://docs.docker.com/) for [Mac](https://docs.docker.com/docker-for-mac/install/) and [Windows](https://docs.docker.com/docker-for-windows/install/download-docker-for-windows)  
![](img/docker.png)

## Usage

##### Clone the repository

        git clone https://github.com/pedrohserrano/fairsharing-metrics.git && \
        cd fairsharing-metrics

##### Build the Docker image

        docker build -t fairsharing-metrics .

##### Run the Docker container

        docker run -it --rm \
        -v "$PWD"/FAIRsharing:/root/FAIRsharing \
        --name=FAIRsharing fairsharing-metrics

(exit the container `exit`)

In case you want to run again an existing container   

        docker start -ai FAIRsharing


## Licence

The MIT License (MIT) 2017

## Acknowledgments

* [RDFUnit](http://aksw.org/Projects/RDFUnit.html)
* [FAIRsharing.org](http://FAIRsharing.org)