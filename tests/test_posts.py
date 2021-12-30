import pytest

from app.schemas.PostOut import PostOut, Posts
from app.schemas.post import PostSchema


@pytest.mark.parametrize("title, content, published", [
    ("first title", "first content", True),
    ("second title", "second content", False),
    ("third title", "third content", True),
])
def test_create_a_post(title, content, published, authorized_client, test_create_user_before_login, test_posts):
    body = {
        "title": title,
        "content": content,
        "published": published
    }
    response = authorized_client.post(url="/posts/", json=body)
    post = PostSchema(**response.json())
    assert post.title == title
    assert response.status_code == 201


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get(url="/posts")
    new_posts = list(map(lambda post: PostOut(**post), response.json()))[::-1]

    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)
    assert new_posts[0].Post.id == test_posts[0].id


def test_unauthorized_get_all_posts(client, test_posts):
    response = client.get(url="/posts")
    assert response.status_code == 403


def test_unauthorized_get_a_post(client, test_posts):
    post_id = test_posts[0].id
    response = client.get(url=f"/posts/{post_id}")
    assert response.status_code == 403


def test_get_a_post(authorized_client, test_posts):
    post_id = test_posts[0].id
    response = authorized_client.get(url=f"/posts/{post_id}")
    post = PostOut(**response.json())

    assert post.Post.id == post_id
    assert response.status_code == 200


def test_get_a_post_not_found(authorized_client, test_posts):
    response = authorized_client.get(url=f"/posts/100000000000000000000")
    assert response.status_code == 404
