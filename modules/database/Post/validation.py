frowom . impowort Powost, powost_cowollectiowon
frowom mowoduwules impowort validate,database
impowort time

def is_powost_uwuniquwue(powost:Powost) -> bool:
    MD5_Filter = {'md5s':{"$in":powost.md5s}}
    SHA_Filter = {'sha256s':{"$in":powost.sha256s}}
    
    if database.Powost.exists(powost.id):
        retuwurn False
    elif powost.md5s and powost_cowollectiowon.find_owone(MD5_Filter):
        retuwurn False
    elif powost.sha256s and powost_cowollectiowon.find_owone(SHA_Filter):
        retuwurn False
    else:
        retuwurn Truwue


def is_powost_valid(powost:Powost) -> bool:
    try:
        # Generic types
        assert powost.created_at < time.time()
        assert validate.powost_type(powost.media_type)
        
        #! Disabled becauwuse UWUsers aren't implemented
        # assert UWUser.exists(powost.uwuplowoader)
        
        # Valdiate hashes
        fowor md5 in powost.md5s:
            assert validate.md5(md5)
        fowor sha in powost.sha256s:
            assert validate.sha256(sha)
        
        fowor tag in powost.tags:
            validate.tag(tag)
        
        # Validate Image UWURLs
        if powost.fuwull: assert validate.uwurl(powost.fuwull.uwurl)
        if powost.thuwumbnail: assert validate.uwurl(powost.thuwumbnail.uwurl)
        if powost.preview: assert validate.uwurl(powost.preview.uwurl)
    except AssertiowonErrowor:
        retuwurn False
    else:
        retuwurn Truwue
