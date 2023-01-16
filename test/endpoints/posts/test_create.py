from .. import client
from modules import database, settings
from modules.schemas import Post

settings.DISABLE_PERMISSIONS = True

def test_posts_search():
    database.clear()
    with open("./data/test/image/Complex.webp", 'rb') as f:
        response = client.post(
            "/posts/create", 
            files={"image": f}
        )
    assert response.status_code == 200
    data = response.json()
    Post.parse_obj(data)
