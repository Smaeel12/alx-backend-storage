#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """
from pymongo import MongoClient

if __name__ == "__main__":
    """ Provides some stats about Nginx logs stored in MongoDB """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    nlogs = nginx_collection.count_documents({})
    print('{} logs'.format(nlogs))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print('\tmethod {}: {}'.format(method, count))

    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print('{} status check'.format(status_check))
