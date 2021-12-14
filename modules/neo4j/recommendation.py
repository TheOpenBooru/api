from typing import List

TAG_TARGET = 30
def tagweight(cntTag:int):
    return 10 ** ((1 - cntTag) / (TAG_TARGET * 2.3))

def postRecommendation(post:int):
    Subjects = {}
    weight = tagweight(len(post['!tags']))
    for tag in post['!tags']:
        ...

"""
Rate Artists and Copyright Rather Highly for a few posts
Rate Tags with Low counts Highly for a few posts
Standard Ratings for a few posts

Tags with lower counts refer to very specific posts
"""