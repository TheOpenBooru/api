from modules.store.s3 import S3Store
from modules import settings
import unittest
import random
import requests

bucket_name = "test-" + settings.STORAGE_S3_BUCKET
method = S3Store(bucket_name)

@unittest.skipIf(settings.AWS_ID == "", reason="No AWS Credentials")
class TestCase(unittest.TestCase):
    def setUp(self):
        if not method.usable:
            raise RuntimeError(method.fail_reason)
            
    def tearDown(self):
        method.clear()


class test_Put_Allows_Data_to_be_Stored(TestCase):
    def test_normal_data(self):
        normal_data = b'MR Foo Bar walked into a bar'
        method.put(normal_data,"normal")
    
    def test_empty_data(self):
        empty_data = b''
        method.put(empty_data,"empty")
        
    def test_large_data(self):
        large_data = random.randbytes(1024*1024)
        method.put(large_data,"large")


class test_Put_Raises_TypeError_for_Invalid_Data(TestCase):
    def test_string(self):
        self.assertRaises(TypeError, method.put, "foobar")
    
    def test_intereger(self):
        self.assertRaises(TypeError, method.put, 0)
    
    def test_python_object(self):
        self.assertRaises(TypeError, method.put, Ellipsis)


class test_Data_is_Retrievable(TestCase):
    def store_and_get(self, data):
        method.put(data, "test_retrieve")
        assert method.get("test_retrieve") == data
        method.delete("test_retrieve")
    
    def test_normal_data(self):
        self.store_and_get(b'example')
    
    def test_special_characters(self):
        self.store_and_get(b'\r\f\n test')


class test_Bad_Key_Should_Raise_Error(TestCase):
    def test_a(self):
        self.assertRaises(FileNotFoundError,method.get,'foobar')


class test_Does_Not_Allow_Path_Traversal(TestCase):
    def test_a(self):
        path = '../../../../../../../../etc/fstab'
        self.assertRaises(FileNotFoundError,method.get,path)


class test_Files_can_be_Accessed_by_URL(TestCase):
    def setUp(self):
        self.key = "test_url"
        self.data = b"example"
        method.put(self.data, self.key)
    def tearDown(self):
        method.delete("test_url")
    
    def test_a(self):
        url = method.url(self.key)
        r = requests.get(url)
        assert r.content == self.data


class test_Deleted_Data_Cant_Be_Obtained(TestCase):
    def setUp(self):
        self.key = "test_delete"
        method.put(b"example",self.key)
    def tearDown(self):
        method.delete(self.key)
    
    def test_a(self):
        method.delete(self.key)
        self.assertRaises(FileNotFoundError,method.get,self.key)


class test_Can_Delete_NonExistant_Keys(TestCase):
    def test_a(self):
        method.delete('foobar')
