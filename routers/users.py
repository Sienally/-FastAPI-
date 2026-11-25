from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from datetime import datetime

# 导入config的session会话
from config.db_config import get_db_session

# 导入crud的user表的增删改查逻辑
from crud.crud_users import crud_select_users, crud_create_user, select_tokens, update_user_info, reset_user_passwd

# 导入utils加密, 密码校验
from utils import security
from utils import auth_token

# 导入utils响应格式
from utils.response import success_response

# 导入schemas的data值构造函数
from schemas.users import UserAuthResponse
# 导入schemas参数规范类
from schemas.users import UserRequest, selectTokensRequest, UserUpdateInfoRequest, UserUpdatePasswordRequest

# 导入models数据库模型类
from models.model_users import Users





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
                "accounts": [{"userName": usr[0].user_name, "token": usr[1].token, "passwd": usr[0].password} for usr in usr_exists]
            }
        if security.auth_passwd(usr.passwd, usr_exists.password):
            # 如果密码也正确
            return {
                "message": "登陆成功",
                "userInfo": {
                    "id": usr_exists.id,
                    "userName": usr_exists.user_name,
                    "token": usr_exists.token,
                    "avatar": usr_exists.avatar,
                    "bio": usr_exists.bio,
                    "gender": usr_exists.gender,
                    "phone": usr_exists.phone if usr_exists.phone is not None else "无"
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
        raise HTTPException(status_code=201, detail="账号已存在")








# ============================== 看所有token接口 ====================================
@router.post("/tokens")
async def get_tokens(obj: selectTokensRequest, db: AsyncSession = Depends(get_db_session)):
    if obj.key == "248311":
        tokens = await select_tokens(db)
        return {
            "info": {"status": "success", "tokens": [{"name": user.user_name, "token": token.token} for user, token in tokens]}
        }
    else:
        return JSONResponse(
            status_code = 401,
            content = {
                "detail": "管理员密码错误"
            }
        )






# ============================== 用户详情信息接口 ====================================
@router.get("/info")
async def get_user_info(user: Users = Depends(auth_token.get_current_user)):
    return {
        "UserInfo": {
            "userName": user.user_name,
            "avatar": user.avatar,
            "bio": user.bio,
            "gender": user.gender,
            "phone": user.phone if user.phone is not None else "无"
        }
    }




# =============================== 更改用户信息接口 ====================================
@router.put("/update")
async def updateUserInfo(
    user_data: UserUpdateInfoRequest,
    user:Users = Depends(auth_token.get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    # 先做token校验, 用户查询(依赖注入) ==> 信息更改 ==> 验证
    user = await update_user_info(db, user.user_name, user_data)
    if user:
        return {
            "info": {
                "userName": user.user_name,
                "info": "用户基本信息修改成功"
            }
        }
    else:
        raise HTTPException(status_code=303, detail="更新失败")






# ============================== 更改用户密码接口 ======================================
@router.put("/resetPassword")
async def reset_password(
    user_obj: UserUpdatePasswordRequest,
    user: Users = Depends(auth_token.get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    # 先判断新旧密码是否一致 ==> 再做token校验, 查询用户(依赖注入) ==> 旧密码校验 ==> 密码更改 ==> 校验
    if user_obj.password == user_obj.new_passwd:
        raise HTTPException(status_code=500, detail="新密码不能与旧密码一致")
    
    # token校验
    status = security.auth_passwd(input_passwd=user_obj.password, passwd=user.password)
    if not status:
        raise HTTPException(status_code=401, detail="密码错误")
    
    # 更新密码操作
    reset_passwd_user = await reset_user_passwd(db, user.user_name, user_obj.new_passwd)
    
    
    if security.auth_passwd(input_passwd=user_obj.new_passwd, passwd=reset_passwd_user.password):
        return {
            "code": 200,
            "status": "success",
            "info": {
                "oldPasswd": user_obj.password,
                "newPasswd": user_obj.new_passwd
            }
        }
    else:
        raise HTTPException(
            status_code = 500,
            detail="密码更新失败"
        )
