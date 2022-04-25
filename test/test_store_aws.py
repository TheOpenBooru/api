from modules.store import aws
import unittest
import random
import requests



@unittest.skipIf(not aws.is_logged_in(), "Not logged into AWS")
class TestCase(unittest.TestCase):
    ...

class test_Put_Allows_Data_to_be_Stored(TestCase):
    def setUp(self):
        self.keys = set()
    def tearDown(self):
        for key in self.keys:
            aws.delete(key)
    
    def test_normal_data(self):
        normal_data = b'MR Foo Bar walked into a bar'
        key = aws.put(normal_data)
        self.keys.add(key)
    
    def test_empty_data(self):
        empty_data = b''
        key = aws.put(empty_data)
        self.keys.add(key)
        
    def test_large_data(self):
        large_data = random.randbytes(1024*1024)
        key = aws.put(large_data)
        self.keys.add(key)

class test_Put_Raises_TypeError_for_Invalid_Data(TestCase):
    def test_string(self):
        self.assertRaises(TypeError, aws.put, "foobar")
    
    def test_intereger(self):
        self.assertRaises(TypeError, aws.put, 0)
    
    def test_python_object(self):
        self.assertRaises(TypeError, aws.put, Ellipsis)

class test_Keys_Should_Be_Unique(TestCase):
    def tearDown(self):
        for key in self.keys:
            aws.delete(key)
    
    def test_a(self):
        self.keys = set()
        for x in range(20):
            data = hex(x).encode()
            key = aws.put(data)
            if key in self.keys:
                self.fail("Key is not unique")
            self.keys.add(key)

class test_Keys_Should_Be_Same_For_Duplicate_Data(TestCase):
    def tearDown(self):
        aws.delete(self.key1)
        aws.delete(self.key2)
    
    def test_duplicate_data(self):
        data = b'example'
        self.key1 = aws.put(data)
        self.key2 = aws.put(data)
        assert self.key1 == self.key2

class test_Keys_Should_Be_Strings(TestCase):
    def tearDown(self):
        aws.delete(self.key)
    
    def test_a(self):
        self.key = aws.put(b'example')
        assert isinstance(self.key,str)

class test_Data_is_Retrievable(TestCase):
    def store_and_get(self, data):
        key = aws.put(data)
        assert aws.get(key) == data
        aws.delete(key)
    
    def test_normal_data(self):
        self.store_and_get(b'example')
    
    def test_special_characters(self):
        self.store_and_get(b'\r\f\n test')

class test_Bad_Key_Should_Raise_Error(TestCase):
    def test_a(self):
        self.assertRaises(FileNotFoundError,aws.get,'foobar')

class test_Does_Not_Allow_Path_Traversal(TestCase):
    def test_a(self):
        path = '../../../../../../../../etc/fstab'
        self.assertRaises(FileNotFoundError,aws.get,path)

class test_Files_can_be_Accessed_by_URL(TestCase):
    def setUp(self):
        self.key = aws.put(b'example')
    def tearDown(self):
        aws.delete(self.key)
    
    def test_a(self):
        url = aws.url(self.key)
        requests.get(url)

class test_Deleted_Data_Cant_Be_Obtained(TestCase):
    def setUp(self):
        self.key = aws.put(b'example')
    def tearDown(self):
        aws.delete(self.key)
    
    def test_a(self):
        aws.delete(self.key)
        self.assertRaises(FileNotFoundError,aws.get,self.key)

class test_Can_Delete_NonExistant_Keys(TestCase):
    def test_a(self):
        aws.delete('foobar')
