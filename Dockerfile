FROM python:3.6

LABEL maintainer "Alexander Malic <alexander.malic@maastrichtuniverstity.nl>" \
      maintainer "Pedro Hernandez <p.hernandezserrano@maastrichtuniverstity.nl>"

#ENV PYTHONPATH /root/NCATS-Translator-DQA

RUN cd && \
    echo 'deb http://http.debian.net/debian jessie-backports main' >> /etc/apt/sources.list && \
    apt update && \
    apt install git -y && \
    apt install maven -y && \
    apt install nano -y && \
    apt install netcat -y && \
    #apt install zsh -y && chsh -s /bin/zsh root && \ 
    pip3 install requests lxml pandas rdflib twine setuptools && \
    apt install -t jessie-backports openjdk-8-jdk -y && \
    update-java-alternatives --set java-1.8.0-openjdk-amd64 && \
    rm /usr/lib/jvm/default-java && ln -s /usr/lib/jvm/java-1.8.0-openjdk-amd64 /usr/lib/jvm/default-java && \
    export JAVA_HOME=/usr/lib/jvm/default-java && \
    git clone https://github.com/AKSW/RDFUnit.git && \
    cd RDFUnit && mvn -pl rdfunit-validate -am clean install -Dmaven.test.skip=true -Dmaven.javadoc.skip=true -Dgpg.skip=true -Dsource.skip=true && \
    mkdir /data-quality-NCATS-translator && \
    #chmod +x ./translator_dqa.py && \
    export JAVA_TOOL_OPTIONS="-Xmx1024m -Xms1024m"

#WORKDIR /root/NCATS-Translator-DQA/ncats_translator_dqa
WORKDIR /root/data-quality-NCATS-translator
#COPY entrypoint.sh ./

#ENTRYPOINT ["/bin/zsh"]
ENTRYPOINT ["/bin/bash"]

#if WORKDIR is RDFUnit then entrypoint ["/RDFUnit/bin/rdfunit"]

EXPOSE 7200
