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
import pytest
import random
from pathlib import Path

def clear():
    for f in Path("./data/files").iterdir():
        f.unlink()

def test_Put_Allows_Data_to_be_Stored(self):
    normal_data = b'MR Foo Bar walked into a bar'
    empty_data = b''
    large_data = random.randbytes(1024*1024)
    
    store.put(normal_data)
    store.put(empty_data)
    store.put(large_data)
    clear()


def test_Put_Raises_TypeError_for_non_bytes_data(self):
    data = [
        'foobar', # string
        0, # int
        Ellipsis, # Python object
        ]
    for x in data:
        self.assertRaises(TypeError, store.put, x)
    clear()


def test_Keys_Should_Be_Unique(self):
    keys = set()
    for x in range(10000):
        data = hex(x).encode()
        key = store.put(data)
        if key in keys:
            self.fail("Key is not unique")
        keys.add(key)
    clear()

def test_Keys_Should_Be_Same_For_Duplicate_Data(self):
    data = b'example'
    key1 = store.put(data)
    key2 = store.put(data)
    assert key1 == key2
    clear()

def test_Keys_Should_Be_Strings(self):
    key = store.put(b'example')
    assert isinstance(key,str)
    clear()

def test_Data_is_Retrievable(self):
    Data = [
        b'example',
        b'\r\f\n test'
    ]
    for x in Data:
        key = store.put(x)
        assert store.get(key) == x
    clear()

def test_NonExistant_Key_Should_Raise_FileNotFoundError(self):
    self.assertRaises(FileNotFoundError,store.get,'foobar')

def test_Deleted_Data_Cant_Be_Obtained(self):
    key = store.put(b'example')
    store.delete(key)
    self.assertRaises(FileNotFoundError,store.get,key)
    clear()

def test_Can_Delete_NonExistant_Keys(self):
    store.delete('foobar')
