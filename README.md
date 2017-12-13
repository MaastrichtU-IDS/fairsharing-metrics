# NCATS Translator
[![License](https://img.shields.io/badge/FAIR-metrics-orange.svg)](http://fairmetrics.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Data Quality Assessment Implementation  |  Docker + RDFUnit

A Dockerization of the NCATS Translator for Data Quality Analysis.   
The purpose of this project is to provide automation of the [NCATS Translator](https://github.com/pedrohserrano/NCATS-Translator-DQA) stand-alone implementation in order to escalate on more general data quality assessment.

## Prerequisites

- Installing [Docker](https://docs.docker.com/) for [Mac](https://docs.docker.com/docker-for-mac/install/) and [Windows](https://docs.docker.com/docker-for-windows/install/download-docker-for-windows)  
![](img/docker.png)

## Usage

##### Clone the repository

        git clone https://github.com/pedrohserrano/data-quality-NCATS-translator.git && \
        cd data-quality-NCATS-translator

##### Build the Docker image

        docker build -t translator_dqa .

##### Run the Docker container

        docker run -it -p 7200:7200 \
        -v "$PWD"/:/root/data-quality-NCATS-translator/ \
        --name=translator_box translator_dqa 

##### Run GraphDB

        ./graphdb.sh


In case you want to keep the container running, then you can make more than one task inside the container, the running command:

        ./translator_dqa.py -d /root/NCATS-Translator-DQA/Input/kegg-drug.ttl

(exit the container `exit`)

In case you want to run again an existing container   

        docker start -ai dqa_box

Notice that we choose `dqa_box` a default name for the container, furthermore, you want to remove it `docker rm dqa_box`

GraphDB is available on  [http://localhost:7200/](http://localhost:7200/)

## Licence

The MIT License (MIT) 2017

## Acknowledgments

* [RDFUnit](http://aksw.org/Projects/RDFUnit.html)
* [FAIRsharing.org](http://FAIRsharing.org)