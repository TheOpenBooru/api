import unittest
from . import driver,Post,User

with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

class Neo4j_Testing(unittest.TestSuite):
    def test_Node_Post(self):
        aHash = '9134669f44c1af0532f613b7508283c4'
        bHash = 'e2fc714c4727ee9395f324cd2e7f331f'
        try:
            PostID = Post.get(hash=aHash)['!id']
            Post.delete(PostID)
        except KeyError:
            pass
        try:
            PostID = Post.get(hash=bHash)['!id']
            Post.delete(PostID)
        except KeyError:
            pass
        
        aID = Post.create('abcd')
        bID = Post.create('dcba')
        try:
            Post.create('abcd')
            Post.create('dcba')
        except KeyError:
            pass
        except Exception:
            raise ValueError("Invalid Error Raised")
        else:
            raise Exception("Duplicate Posts Created")
        assert 'abcd' == (a := Post.get(id=aID)['md5'])
        assert 'abcd' == (b := Post.get(id=bID)['md5'])
        assert a == Post.get(id=aID)
        assert b == Post.get(id=bID)
        assert a == Post.get(hash='abcd')
        assert b == Post.get(hash='dcba')

        KEYS = ("!id","created_at","md5","source",
                "!views","!favourite","!blocked","!creator","!comments","!tags")
        for key in KEYS:
            assert key in a, f"Missing The Key[{key}]"
        Post.delete(aID)
        Post.delete(bID)

    def test_Node_User(self):
        aName = 'Foo'
        bName = 'Bar'
        try:
            UserID = User.get(name=aName)['!id']
            User.delete(UserID)
        except KeyError:
            pass
        try:
            UserID = User.get(name=bName)['!id']
            User.delete(UserID)
        except KeyError:
            pass
        aID = User.create(aName)
        bID = User.create(bName)
        try:
            User.create(aName)
            User.create(bName)
        except KeyError:
            pass
        except Exception:
            raise ValueError("Invalid Error Raised")
        else:
            raise Exception("Duplicate Posts Created")
        
        assert aName == (a := User.get(id=aID))['name']
        assert bName == (b := User.get(id=bID))['name']
        assert a == User.get(id=aID)
        assert b == User.get(id=bID)
        assert a == User.get(name=aName)
        assert b == User.get(name=bName)

        KEYS = ("created","name","avatar_url","description",
                "!id","!posts","!history","!comments")
        for key in KEYS:
            assert key in a, f"Missing The Key[{key}]"
        for key in a:
            assert key in KEYS, f"Additional Key[{key}]"
            
        User.delete(aID)
        User.delete(bID)

