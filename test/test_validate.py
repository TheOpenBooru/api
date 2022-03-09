import unittest
from modules import validate


def test_validate_allows_valid_md5(self):
    valid = [
        ("c3499c2729730a7f807efb8676a92dcb","Lowercase"),
        ("C3499C2729730A7F807EFB8676A92DCB","Uppercase"),
        ("c3499c2729730A7F807EFB8676A92Dcb","MixedCase"),
    ]
    for valid,reason in valid:
        assert validate.md5(valid) == True,reason

def test_validate_denies_invalid_md5(self):
    invalid = [
        ("c3499C2729730a7F807EdB8676A92DC", "Too Short"),
        ("c3499C2729730a7F807EdB8676A92DCDD", "Too Long"),
        ("c3499C2729730a7F807EdB8676A92DCG", "Wrong Char"),
    ]
    for invalid,reason in invalid:
        assert validate.md5(invalid) == False,reason


def test_validate_allows_valid_sha256():
    valid = [
        ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340fa',"Normal")
    ]
    for valid,reason in valid:
        assert validate.sha256(valid) == True,reason

def test_validate_denies_invalid_sha256():
    invalid = [
        ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340faa',"Too Long"),
        ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340f',"Too Short"),
        ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340fG',"Wrong Char"),
    ]
    for invalid,reason in invalid:
        assert validate.sha256(invalid) == False,reason


def test_validate_allows_valid_urls():
    valid = [
        ("https://example", "No TLD"),
        ("https://www.example.com", "Normal"),
        ("https://long.amount.of.prefix.example.com", "Many prefixes"),
        ("https://example.com", "No Prefix"),
        ("https://www.example.co.uk","double TLD"),
        ("http://www.example.com", "http"),
        ("https://www.example.com?a=2", "Parameter"),
    ]
    for valid,reason in valid:
        assert validate.url(valid) == True,reason

def test_validate_denies_invalid_urls():
    invalid = [
        ("https//example.com", "No semi-colon"),
        ("https:/example.com", "Single slash"),
        ("https:/example.com//", "Double Slash"),
        ("example.com", "No Protocol"),
    ]
    for invalid,reason in invalid:
        assert validate.url(invalid) == False,reason


def test_validate_allows_valid_emails():
    valid = [
        ("david@example.com","Regular"),
        ("l@example.com","Single Character"),
    ]
    for valid,reason in valid:
        assert validate.email(valid) == True,reason

def test_validate_denies_invalid_emails():
    invalid = [
        ("@example.com","No Username"),
        ("test@example","No TLD"),
        ("test@","No Hostname"),
    ]
    for invalid,reason in invalid:
        assert validate.email(invalid) == False,reason

def test_validate_allows_valid_usernames():
    valid = [
        ('abcdefigjklmnopqrstuvwxyz',"Valid Alphabet"),
        ('0123456789_',"Valid Punctionation"),
        ('f'*4,"Min Length"),
        ('f'*32, "Max Length"),
    ]
    for valid,reason in valid:
        assert validate.username(valid) == True,reason

def test_validate_denies_invalid_usernames():
    invalid = [
        ('f'*3, "Too Short"),
        ('f'*33, "Too Long"),
        ('оabcdefgh', "Homograph o"),
    ]
    for invalid,reason in invalid:
        assert validate.username(invalid) == False,reason


def test_validate_allows_valid_languages():
    valid = [
        ("vie","Obscure"),
        ("fry","Obscure"),
        ("que","Obscure"),
        ("eng","English")
    ]
    for valid, reason in valid:
        assert validate.language(valid) == True,reason

def test_validate_denies_invalid_languages():
    invalid = [
        ('qaa', "Always Invalid Name"),
        ('english', "Full Name"),
        ('en', "ISO 639-1 code, not 3 characters"),
        ('', "Empty String"),
    ]
    for invalid,reason in invalid:
        assert validate.language(invalid) == False,reason
