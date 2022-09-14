from modules import database, schemas


def test_Tag_Parents_Search():
    database.Tag.clear()
    database.Tag.insert(schemas.Tag(
        name="super_mario", parents=[]
    ))
    database.Tag.insert(schemas.Tag(
        name="peach", parents=["super_mario"]
    ))
    database.Tag.insert(schemas.Tag(
        name="mario", parents=["super_mario"]
    ))
    image = schemas.Image(
        width=1,
        height=1,
        mimetype="image/png",
        url=""
    )
    post = schemas.Post(
        id=database.Post.generate_id(),
        media_type=schemas.MediaType.image,
        full=image,
        thumbnail=image,
        tags=["mario","peach"]
    )
    database.Post.insert(post)

    assert post in database.Post.search(schemas.PostQuery(
        include_tags=["super_mario"]
    ))
    
    assert post in database.Post.search(schemas.PostQuery(
        include_tags=["mario"]
    ))