from modules import posts,schemas
import json

with open('./data/test/sample_data.json','r') as f:
    TESTDATA = json.load(f)

TEST_VIDEO = TESTDATA['video']['heavy']
TEST_ANIMATION = TESTDATA['animation']['Transparent']
TEST_IMAGE = TESTDATA['image']['Small']
