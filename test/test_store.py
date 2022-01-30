"""Requirements:
- [x] It should store data at the key
- [x] Storing a duplicate key should raise a FileExistsError
- [x] Data should be accessible via a URL
- [X] URL for a non-existent key should raise a FileNotFoundError
- [X] Getting Data via the key
- [X] Data should not be changed
- [X] Getting a non-existent key should raise a FileNotFoundError
- [] Data should be deletedable via the key
- [] You should be able to delete a non-existent key
"""
from modules import store
import unittest
import requests


class test_Store_Data_At_Key(unittest.TestCase):
    def tearDown(self):
        store.delete('example_key')
    def test_Store_Data_At_Key(self):
        store.put('example_key',  b'example_data')

class test_Duplicate_Keys_Should_Raise_Error(unittest.TestCase):
    def tearDown(self):
        store.delete('example_key')
    def test_Store_Duplicate_Data(self):
        store.put('example_key', b'test')
        self.assertRaises(FileExistsError,store.put,'example_key', b'test')

class test_URL_Should_Be_Valid(unittest.TestCase):
    data = b'example_data'
    def setUp(self):
        store.put('example_key', self.data)
    def tearDown(self):
        store.delete('example_key')
    def test_URL_Should_Be_Valid(self):
        url = store.url('example_key')
        self.assertRegex(url,r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
    def test_URL_Should_Reference_Data(self):
        url = store.url('example_key')
        r = requests.get(url)
        self.assertEquals(r.content,self.data,r.text)


class test_Data_Is_Retrievable(unittest.TestCase):
    def tearDown(self):
        store.delete('example_key')
    def test_Store_Data_At_Key(self):
        data = b'example_data'
        store.put('example_key', data)
        self.assertEquals(data,store.get('example_key'))

class test_Invalid_Key_Should_Raise_Error(unittest.TestCase):
    def test_Invalid_Get_Key_Should_Raise_Error(self):
        self.assertRaises(FileNotFoundError,store.get,'non_existent_key')
    def test_Invalid_URL_Key_Should_Raise_Error(self):
        self.assertRaises(FileNotFoundError,store.url,'non_existent_key')

class test_Stored_Data_Shouldnt_Be_Changed(unittest.TestCase):
    data = b'Example\r\nData \n'
    def setUp(self):
        store.put('example_key', self.data)
    def tearDown(self):
        store.delete('example_key')
    def test_Data_Is_Same(self):
        store.put('example_key', self.data)
        self.assertEqual(store.get('example_key'), self.data)

class test_Data_Should_Be_Deletable(unittest.TestCase):
    data = b'Example Data'
    def setUp(self):
        store.put('example_key', self.data)
    def test_Deleting_Key(self):
        store.delete('example_key')
        self.assertRaises(FileNotFoundError,store.get,'example_key')
