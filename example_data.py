import json
import requests
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

from modules import neo4j

tagIDs = {}
userIDs = {}
with open('data/sampledata.json') as f:
    data = json.load(f)

def main():
    for i,post in tqdm(list(enumerate(data))):
        try:
            pID = neo4j.Post.create(post['hash'])
        except KeyError:
            continue

        creatorName = post['owner']
        if creatorName:
            if creatorName not in userIDs:
                user = neo4j.User.get(name=creatorName)
                if user:
                    uID = user['id']
                else:
                    uID = neo4j.User.create(creatorName)
                userIDs[creatorName] = uID
            neo4j.CreatedPost.add(userIDs[creatorName],pID)
        
        tagsToAdd = []
        for tagName in post['tags'].split(' '):
            if not tagName:
                continue
            if tagName not in tagIDs:
                tag = neo4j.Tag.get(name=tagName)
                if tag:
                    tID = tag['id']
                else:
                    tID = neo4j.Tag.create(name=tagName)
                tagIDs[tagName] = tID
            tagsToAdd.append(tagIDs[tagName])

        Tagged.bulk_add(pID,tagsToAdd)

if __name__ == '__main__':
    main()