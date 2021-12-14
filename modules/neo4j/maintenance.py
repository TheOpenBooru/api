from . import driver

def ExpungeOutdatedViews():
    raise NotImplementedError

def CheckCommentValidity():
    raise NotImplementedError

def DetectInvalidIds():
    with driver.session() as tx:
        response = tx.run("""
            MATCH (n)
                WHERE n.id <> ID(n)
            RETURN n
            """).data()

def DetectTagSiblings():
    pass
    # Where tags are spotted majority with each other
    # Tag1, Tag2, Tag4
    # Tag1, Tag2, Tag6
    # Tag1, Tag2, Tag3
    # Tag1, Tag2, Tag9

def DetectTagParents():
    pass
    # Where a tag majoritily has another tag, but not the way around
    # e.g.
    # Tag1,Tag2
    # Tag1,Tag2
    # Tag2,Tag3
