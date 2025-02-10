from typing import Annotated

from fastapi import Depends

from .database import get_db, DBManager
from .redis import get_redis_db, RedisManager

SessionDep = Annotated[DBManager, Depends(get_db)]
RedisDep = Annotated[RedisManager, Depends(get_redis_db)]