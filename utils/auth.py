from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# 导入会话
from config.db_config import get_db_session

# 导入查询业务
from crud import crud_users



# 校验token的通用工具函数
async def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
    db: AsyncSession = Depends(get_db_session)
):
    token = authorization.split(" ")[1]
    user = await crud_users.select_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="无效或过期的令牌")
    
    return user