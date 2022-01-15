"""Requirements:
- It should store data at the key
- Storing a duplicate key should raise a FileExistsError
- This data should be retreivable via the key
- Data should be accessible via a URL
- Stored Data should not be changed
- Retrieveing a non-existent key should raise a FileNotFoundError
- Data should be deletedable via the key
- You should be able to delete a non-existent key
"""
from modules import store
import unittest
import requests

store.delete('example_key')
class test_Store_Data_At_Key(unittest.TestCase):
    def tearDown(self):
        store.delete('example_key')
    def test_Store_Data_At_Key(self):
        data = b'example_data'
        store.put('example_key', data)

class test_Duplicate_Keys_Should_Raise_Error(unittest.TestCase):
    def tearDown(self):
        store.delete('example_key')
    def test_Store_Duplicate_Data(self):
        data = b'example_data'
        store.put('example_key', data)
        self.assertRaises(FileExistsError,store.put,'example_key', data)

class test_URL_Should_Be_Valid(unittest.TestCase):
    def tearDowN(self):
        store.delete('example_key_1')
        store.delete('example_key_2')
    def test_URL_Should_Be_Valid(self):
        store.put('example_key_1', b'example_data')
        url = store.url('example_key_1')
        self.assertRegex(url,r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
    def test_URL_Should_Reference_Data(self):
        data = b'test_example_data'
        store.put('example_key_2', data)
        url = store.url('example_key_2')
        r = requests.get(url)
        self.assertEquals(r.content,data,r.text)


class test_Data_Is_Retrievable(unittest.TestCase):
    def setUp(self):
        store.delete('example_key')
    def test_Store_Data_At_Key(self):
        data = b'example_data'
        store.put('example_key', data)
        self.assertEquals(data,store.get('example_key'))


class test_Stored_Data_Shouldnt_Be_Changed(unittest.TestCase):
    def setUp(self):
        store.delete('example_key')
        store.delete('example_key_crlf')
    
    def test_Data_Is_Same(self):
        data = b'Example\r\nData \n'
        store.put('example_key', data)
        self.assertEqual(store.get('example_key'), data)
        
    def test_CRLF_Shouldnt_Be_Changed(self):
        data = b'Example\r\nData \n'
        store.put('example_key_crlf', data)
        self.assertEqual(store.get('example_key_crlf'), data)