FROM python:3.5

LABEL maintainer "Pedro Hernandez <p.hernandezserrano@maastrichtuniverstity.nl>"

WORKDIR /app

COPY FAIRsharing/ /app

RUN sed -i -e 's/\r$//' *

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/app/scrapper_metrics.py"]
