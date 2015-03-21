#!/bin/bash

# python pip source
curl -O https://pypi.python.org/packages/source/p/pip/pip-6.0.8.tar.gz#md5=2332e6f97e75ded3bddde0ced01dbda3
mv pip-6.0.8.tar.gz#md5=2332e6f97e75ded3bddde0ced01dbda3 ipython3/pip-6.0.8.tar.gz

# python ipython
curl -O https://pypi.python.org/packages/source/i/ipython/ipython-3.0.0.tar.gz#md5=b3f00f3c0be036fafef3b0b9d663f27e
mv ipython-3.0.0.tar.gz#md5=b3f00f3c0be036fafef3b0b9d663f27e ipython3/ipython-3.0.0.tar.gz

# python bson
# curl -O https://pypi.python.org/packages/source/b/bson/bson-0.3.3.tar.gz#md5=46bce086741b651afaba0ea118fc5f8d
# mv bson-0.3.3.tar.gz#md5=46bce086741b651afaba0ea118fc5f8d socketServer/bson-0.3.3.tar.gz

# python pymongo
curl -O https://pypi.python.org/packages/source/p/pymongo/pymongo-2.8.tar.gz#md5=23100361c9af1904eb2d7722f2658114
mv pymongo-2.8.tar.gz#md5=23100361c9af1904eb2d7722f2658114 socketServer/pymongo-2.8.tar.gz
