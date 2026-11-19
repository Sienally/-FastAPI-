from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from datetime import datetime

# 导入会话
from config.db_config import get_db_session

# 导入user表的增删改查逻辑
from crud.users import crud_select_users, crud_create_user, create_token, select_user_by_token, select_tokens

# 导入参数规范类
from schemas.users import UserRequest

# 导入加密, 密码校验
from utils import security

# 导入响应格式
from utils.response import success_response

# 导入data值构造函数
from schemas.users import UserAuthResponse





router = APIRouter(prefix="/api/users", tags=["users"])




# ===============================登录接口======================================
@router.post("/login")
async def get_account(usr: UserRequest, db: AsyncSession = Depends(get_db_session)):

    # 先检测账号是否存在
    usr_exists = await crud_select_users(db, usr.user_name, usr.passwd, usr.key)
    
    # 账号存在
    if usr_exists:
        if usr.key == "248311":
            return {
                "message": "查询全部",
                "accounts": [{"userName": usr.user_name, "passwd": usr.password} for usr in usr_exists]
            }
        if security.auth_passwd(usr.passwd, usr_exists.password):
            # 如果密码也正确
            return {
                "message": "登陆成功",
                "userInfo": {
                    "id": usr_exists.id,
                    "userName": usr_exists.user_name,
                    "avatar": usr_exists.avatar,
                    "bio": usr_exists.bio,
                    "gender": usr_exists.gender,
                    "phone": usr_exists.phone
                }
            }
        else:
            # 密码错误
            raise HTTPException(status_code=501, detail="密码错误")
    # 账号不存在
    else:
        raise HTTPException(status_code=401, detail="账号不存在")





# ===============================注册接口======================================
@router.post("/signUp")
async def create_user(usr: UserRequest, db: AsyncSession = Depends(get_db_session)):
    token = await crud_create_user(db, usr)
    if token:
        return {
            "isok": 1,
            "message": "注册成功",
            "userInfo": {
                "token": token,
                "userName": usr.user_name,
                "bio": usr.bio,
                "avatar": usr.avatar
            }
        }
    else:
        raise HTTPException(status_code=401, detail="账号已存在")








# ============================== 看所有token接口 ====================================
@router.post("/tokens")
async def get_tokens(usr: UserRequest, db: AsyncSession = Depends(get_db_session)):
    if usr.key == "248311":
        tokens = await select_tokens(db)
        return {
            "tokens": {"tokens": [{"name": user.user_name, "token": token.token} for user,token in tokens]}
        }
    else:
        return JSONResponse(
            status_code = 401,
            content = {
                "detail": "管理员密码错误"
            }
        )






# ============================== 用户详情信息接口 ====================================
@router.post("/info")
async def get_user_info(usr: UserRequest, db: AsyncSession = Depends(get_db_session)):
    # token校验 ==> 查找用户
    user = await select_user_by_token(db, usr.token)
    if user:
        return {
            "UserInfo": {
                "userName": user.user_name,
                "avatar": user.avatar,
                "bio": user.bio,
                "gender": user.gender,
                "phone": user.phone if user.phone is not None else "无"
            }
        }
    else:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "token失效",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )