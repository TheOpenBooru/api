"""Requirements:
- Send must raise ValueError if the to address is invalid
- Send must raise ValueError if the subject is too long
"""

import unittest
from modules import email


VALID_EMAIL = "test@example.com"

class test_To_Address_Validated_Correctly(unittest.TestCase):
    def test_Error_Raised_On_Invalid_Address(self):
        Invalid_Email_Addresses = [
            'test@', # No Hostname
            'test@example', # No TLD
            'example.com', # No user
            '', # Empty
        ]
        for EMAIL in Invalid_Email_Addresses:
            self.assertRaises(ValueError,email.send,
                EMAIL,
                'example subject',
                '<a href="{{ link }}">{{ link }}</a>',
                link='https://www.example.com'
            )
            
    def test_No_Error_Raised_On_Valid_Address(self):
        Valid_Email_Addresses = [
            'test@example.com'
        ]
        for EMAIL in Valid_Email_Addresses:
            email.send(EMAIL,'subject','password_reset.html',link='https://www.example.com')

class test_Email_Wont_Accept_Abnormal_Subject_Length(unittest.TestCase):
    def test_Error_Raised_On_Too_Long_Address(self):
        subject = 'f'*79
        self.assertRaises(ValueError, email.send,'test@example.com',subject,'',link='https://www.example.com')
    def test_Max_Legnth_Accepted(self):
        subject = 'f'*78
        email.send('test@example.com',subject,'',link='https://www.example.com')

class test_Send_Password_Reset(unittest.TestCase):
    def test_send(self):
        email.send_password_reset(
            'benbrady04.bb@gmail.com',
            'David Bowie',
            'https://www.example.com'
        )