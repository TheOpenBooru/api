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
    normalData = b'MR Foo Bar walked into a bar'
    smallData = b''
    largeData = random.randbytes(1024*1024)
    def test_a(self):
        store.put(self.normalData)
        store.put(self.smallData)
        store.put(self.largeData)
    def tearDown(self) -> None:
        clear()

class test_Put_Raises_TypeError_for_non_bytes_data(unittest.TestCase):
    def test_invalid_data(self):
        data = [
            'foobar',
            0,
            Ellipsis,
            ]
        for x in data:
            self.assertRaises(TypeError, store.put, x)
    def tearDown(self) -> None:
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
    def tearDown(self) -> None:
        clear()

class test_Keys_Should_Be_Same_For_Duplicate_Data(unittest.TestCase):
    def test_duplicate_data(self):
        data = b'example'
        key1 = store.put(data)
        key2 = store.put(data)
        self.assertEquals(key1,key2)
    def tearDown(self) -> None:
        clear()

class test_Keys_Should_Be_Strings(unittest.TestCase):
    def test_a(self):
        key = store.put(b'example')
        self.assertIsInstance(key, str)
    def tearDown(self) -> None:
        clear()

class test_Data_is_Retrievable(unittest.TestCase):
    def test_a(self):
        Data = [
            b'example',
            b'\r\f\n test'
        ]
        for x in Data:
            key = store.put(x)
            self.assertEquals(store.get(key),x)
    def tearDown(self):
        clear()

class test_NonExistant_Key_Should_Raise_FileNotFoundError(unittest.TestCase):
    def test_a(self):
        self.assertRaises(FileNotFoundError,store.get,'foobar')

class test_Deleted_Data_Cant_Be_Obtained(unittest.TestCase):
    def test_a(self):
        key = store.put(b'example')
        store.delete(key)
        self.assertRaises(FileNotFoundError,store.get,key)
    def tearDown(self):
        clear()

class test_Can_Delete_NonExistant_Keys(unittest.TestCase):
    def test_a(self):
        store.delete('foobar')
