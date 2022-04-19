from modules.store import local
import unittest
import random
from pathlib import Path


class test_Put_Allows_Data_to_be_Stored(unittest.TestCase):
    def tearDown(self):
        local.clear()
    
    def test_normal_data(self):
        normal_data = b'MR Foo Bar walked into a bar'
        local.put(normal_data)
    
    def test_empty_data(self):
        empty_data = b''
        local.put(empty_data)
        
    def test_large_data(self):
        large_data = random.randbytes(1024*1024)
        local.put(large_data)

class test_Put_Raises_TypeError_for_Invalid_Data(unittest.TestCase):
    def tearDown(self):
        local.clear()
    
    def test_string(self):
        self.assertRaises(TypeError, local.put, "foobar")
    
    def test_intereger(self):
        self.assertRaises(TypeError, local.put, 0)
    
    def test_python_object(self):
        self.assertRaises(TypeError, local.put, Ellipsis)

class test_Keys_Should_Be_Unique(unittest.TestCase):
    def tearDown(self):
        local.clear()
    
    def test_a(self):
        keys = set()
        for x in range(10000):
            data = hex(x).encode()
            key = local.put(data)
            if key in keys:
                self.fail("Key is not unique")
            keys.add(key)

class test_Keys_Should_Be_Same_For_Duplicate_Data(unittest.TestCase):
    def tearDown(self):
        local.clear()
    
    def test_duplicate_data(self):
        data = b'example'
        key1 = local.put(data)
        key2 = local.put(data)
        assert key1 == key2

class test_Keys_Should_Be_Strings(unittest.TestCase):
    def tearDown(self):
        local.clear()
    
    def test_a(self):
        key = local.put(b'example')
        assert isinstance(key,str)

class test_Data_is_Retrievable(unittest.TestCase):
    def tearDown(self):
        local.clear()
    
    def store_and_get(self, data):
        key = local.put(data)
        assert local.get(key) == data
    
    def test_normal_data(self):
        self.store_and_get(b'example')
    
    def test_special_characters(self):
        self.store_and_get(b'\r\f\n test')

class test_Bad_Key_Should_Raise_Error(unittest.TestCase):
    def test_a(self):
        self.assertRaises(FileNotFoundError,local.get,'foobar')

class test_Does_Not_Allow_Path_Traversal(unittest.TestCase):
    def test_a(self):
        path = '../../../../../../../../etc/fstab'
        self.assertRaises(FileNotFoundError,local.get,path)

class test_Deleted_Data_Cant_Be_Obtained(unittest.TestCase):
    def tearDown(self):
        local.clear()
    
    def test_a(self):
        key = local.put(b'example')
        local.delete(key)
        self.assertRaises(FileNotFoundError,local.get,key)

class test_Can_Delete_NonExistant_Keys(unittest.TestCase):
    def test_a(self):
        local.delete('foobar')
