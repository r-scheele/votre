from app.routers import posts, users
from app.routers.auth import auth


def set_router(app):
    app.include_router(posts.router)
    app.include_router(users.router)
    app.include_router(auth.router)
