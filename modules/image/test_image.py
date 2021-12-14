from . import _s3 as s3
from . import _local as local 

import unittest
import random

class S3(unittest.TestCase):
    def scenario_1(self):
        name = hex(random.getrandbits(32))
        
        with open('./data/test/example.jpg','rb') as f:
            data = f.read()
        
        s3.put(name,data)
        try:
            s3.put(name,data)
        except FileExistsError:
            pass
        else:
            raise FileExistsError("Allowed Duplicate File")
        
        assert s3.get(name) == data, "Data Retried Didn't match original"
        s3.delete(name)
        try: s3.get(name)
        except FileNotFoundError: pass
        else: raise FileNotFoundError('No KeyError Raised for Getting Invalid Object')