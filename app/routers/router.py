from app.routers import posts, users, likes, comments
from app.routers.auth import auth


def set_router(app):

    app.include_router(users.router)
    app.include_router(auth.router)
    app.include_router(posts.router)
    app.include_router(likes.router)
    app.include_router(comments.router)
