FROM python:3.5

LABEL maintainer "Pedro Hernandez <p.hernandezserrano@maastrichtuniverstity.nl>"

WORKDIR /root/FAIRsharing

COPY FAIRsharing/ ./

RUN sed -i -e 's/\r$//' *

RUN pip install -r requirements.txt

ENTRYPOINT ["./execute.sh"]
