"""Requirements:
- Data is storable via put
- Put raises TypeError for non-bytes data
- Keys should be strings
- Keys should be the same for duplicate data
- Keys should be unique among different data
- Data should not be changed when stored
- Get should raise a FileNotFoundError for a non-existent key
- Data should be deletedable via delete
- Non-Existant Keys Are Deletable
- Deleted Data should not be retrievable
"""

from modules import store
import unittest
import random
from pathlib import Path

def clear():
    for f in Path("./data/files").iterdir():
        f.unlink()

class test_Put_Allows_Data_to_be_Stored(unittest.TestCase):
    def test_a(self):
        normal_data = b'MR Foo Bar walked into a bar'
        empty_data = b''
        large_data = random.randbytes(1024*1024)
        
        store.put(normal_data)
        store.put(empty_data)
        store.put(large_data)
        clear()

class test_Put_Raises_TypeError_for_non_bytes_data(unittest.TestCase):
    def test_invalid_data(self):
        data = [
            'foobar', # string
            0, # int
            Ellipsis, # Python object
            ]
        for x in data:
            self.assertRaises(TypeError, store.put, x)
        clear()

class test_Keys_Should_Be_Unique(unittest.TestCase):
    def test_a(self):
        keys = set()
        for x in range(10000):
            data = hex(x).encode()
            key = store.put(data)
            if key in keys:
                self.fail("Key is not unique")
            keys.add(key)
        clear()

class test_Keys_Should_Be_Same_For_Duplicate_Data(unittest.TestCase):
    def test_duplicate_data(self):
        data = b'example'
        key1 = store.put(data)
        key2 = store.put(data)
        assert key1 == key2
        clear()

class test_Keys_Should_Be_Strings(unittest.TestCase):
    def test_a(self):
        key = store.put(b'example')
        assert isinstance(key,str)
        clear()

class test_Data_is_Retrievable(unittest.TestCase):
    def test_a(self):
        Data = [
            b'example',
            b'\r\f\n test'
        ]
        for x in Data:
            key = store.put(x)
            assert store.get(key) == x
        clear()

class test_NonExistant_Key_Should_Raise_FileNotFoundError(unittest.TestCase):
    def test_a(self):
        self.assertRaises(FileNotFoundError,store.get,'foobar')

class test_Deleted_Data_Cant_Be_Obtained(unittest.TestCase):
    def test_a(self):
        key = store.put(b'example')
        store.delete(key)
        self.assertRaises(FileNotFoundError,store.get,key)
        clear()

class test_Can_Delete_NonExistant_Keys(unittest.TestCase):
    def test_a(self):
        store.delete('foobar')
