from typing import Annotated

from fastapi import Depends

from .database import get_db, DBManager

SessionDep = Annotated[DBManager, Depends(get_db)]
