#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys,getopt

from elasticsearch import Elasticsearch
es = None

def initEs(active):
    global es
    if "test" in active:
        es = Elasticsearch(hosts=["10.4.19.41:9200"])
    elif "prod" in active:
        es = Elasticsearch(hosts=["10.5.25.80:9200", "10.5.25.79:9200", "10.5.25.78:9200"], http_auth=("elastic", "order20210508"))
    elif "dev" in active:
        es = Elasticsearch(hosts=["10.4.19.41:9200"])


