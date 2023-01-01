from openbooru.modules import tags, database, schemas

def test_Load_Tag_Data():
    database.clear()
    tag = schemas.Tag(name="dragon")
    tags.import_e621_tag_data()