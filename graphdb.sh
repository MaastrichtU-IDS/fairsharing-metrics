#!/bin/bash

echo runing graphdb ... 
cp graphdb-free-8.3.1-dist.zip /root/graphdb-free-8.3.1-dist.zip
cd && unzip graphdb-free-8.3.1-dist.zip
echo "LC_ALL=en_US.UTF-8" >> /etc/environment
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
locale-gen en_US.UTF-8
./graphdb-free-8.3.1/bin/graphdb -d
cd data-quality-NCATS-translator
echo go to http://localhost:7200/