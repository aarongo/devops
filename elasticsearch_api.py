#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu


from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts="10.200.200.80")

# print es.index(index="logstash-restapi-access-2017.11.01", doc_type="restapi-access", id='AV92NUH5wssJ5dzcFDTD', body={"any": "data", "timestamp": datetime.now()})
# a = es.get(index="logstash-restapi-access-2017.11.01", doc_type="restapi-access", id='AV92NUH5wssJ5dzcFDTD')
# print a


res = es.search(index="logstash-restapi-access-2017.11.01", body={"query": {
    "bool": {"must": [{"query_string": {"default_field": "status", "query": "404"}}], "must_not": [], "should": []}},
                                                                  "from": 0, "size": 10, "sort": [], "aggs": {}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print hit['_source']
