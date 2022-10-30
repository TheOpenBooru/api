from .. import client
from modules import account, database
from modules.schemas import Post

def test_posts_search():
    database.clear()
    with open("./data/test/image/Complex.webp") as f:
        response = client.post(
            "/posts/create", 
            files={"image": f}
        )
    assert response.status_code == 200
    data = response.json()
    Post.parse_obj(data)
