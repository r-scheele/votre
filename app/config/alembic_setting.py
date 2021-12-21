from app.models.users import Base as UserBase
from app.models.posts import Base as PostBase
from app.models.comments import Base as CommentBase
from app.models.likes import Base as LikeBase

bases = [UserBase.metadata, PostBase.metadata, CommentBase.metadata, LikeBase.metadata]
