from .. import ExamplePost, ExampleTag
import json
import pytest
from modules import schemas, database

with open('data/test/sample_data.json','r') as f:
    TESTDATA = json.load(f)

TEST_VIDEO = TESTDATA['video']['heavy']
TEST_ANIMATION = TESTDATA['animation']['Transparent']
TEST_IMAGE = TESTDATA['image']['Small']
