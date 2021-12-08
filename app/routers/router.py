from app.routers import posts, users, auth


def set_router(app):
    app.include_router(posts.router)
    app.include_router(users.router)
    app.include_router(auth.router)
