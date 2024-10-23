#!/usr/bin/env python3
""" 12-log_stats.py """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    count = len(list(nginx_collection.find()))
    get = len(list(nginx_collection.find({"method": "GET"})))
    post = len(list(nginx_collection.find({"method": "POST"})))
    put = len(list(nginx_collection.find({"method": "PUT"})))
    patch = len(list(nginx_collection.find({"method": "PATCH"})))
    delete = len(list(nginx_collection.find({"method": "DELETE"})))
    status = len(list(nginx_collection.find({"path": "/status"})))
    print("""\
{} logs
Methods:
    method GET: {}
    method POST: {}
    method PUT: {}
    method PATCH: {}
    method DELETE: {}
{} status check\
""".format(count, get, post, put, patch, delete, status))
