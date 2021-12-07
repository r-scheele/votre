from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


posts = [
    {"title": "This is a title", "content": "The content of the post", "id": 1},
    {"title": "This is a title of second", "content": "The content of the post 2", "id": 2}
]


@app.get(path="/")
def root():
    return {"message": "Hello World"}


@app.get(path="/posts/{post_id}")
def get_post(post_id: int):
    post = None
    for p in posts:
        if p["id"] == post_id:
            post = p
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} is not found")
    return {"data": post}


@app.get("/posts")
def get_posts():
    return {"data": posts}


@app.post(path="/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post_id = len(posts) + 1
    new_post = post.dict()
    new_post["id"] = new_post_id

    posts.append(new_post)

    return {
        "message": "Posts successfully created",
        "post": posts
    }


@app.put(path="posts/{post_id}")
def update_post(post_id: int, post: Post):
    # update post logic
    pass


@app.delete(path="posts/{post_id", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    # some logic to delete post
    return Response(status_code=status.HTTP_204_NO_CONTENT)
