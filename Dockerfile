FROM python:3.5

LABEL maintainer "Pedro Hernandez <p.hernandezserrano@maastrichtuniverstity.nl>"

COPY FAIRsharing /root/FAIRsharing

WORKDIR /root/FAIRsharing

RUN pip install -r requirements.txt

#CMD [ "python", "scrapper_metrics.py" ]
ENTRYPOINT ["./execute.sh"]