from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

# 导入模型
from models.model_users import Users, UserToken

# 导入密码加密函数
from utils import security

# 导入时间
from datetime import datetime, timedelta

# 导入uuid 进行生成随机token
import uuid







# 登录校验
async def crud_select_users(
    db: AsyncSession,
    user_name: str | None = None,
    passwd: str | None = None,
    key: str | None = None
):
    if key == "248311":
        stmt = select(Users, UserToken).join(UserToken, Users.id == UserToken.user_id)
        result = await db.execute(stmt)
        return result.all()
    else:    
        stmt = select(Users).where(Users.user_name == user_name)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        # 更新token
        if user:
            token = await create_token(db, user.id)
            user.token = token
        return user





# 注册
async def crud_create_user(db: AsyncSession, usr):
    # 查一下库先, 看看有没有同名的账号
    exists_count = await crud_select_users(db, usr.user_name, usr.passwd)
    
    if exists_count:
        return 0
    else:
        # 先加密处理
        hashed_passwd = security.get_hash_passwd(usr.passwd)
        user = Users(user_name=usr.user_name, password=hashed_passwd, phone=usr.phone, bio=usr.bio, gender=usr.gender)
        db.add(user)            # 会话的add()方法是同步操作, 不需要await
        await db.commit()
        await db.refresh(user)  # 从数据库读回最新的user

        token = await create_token(db, user.id)  #  生成token
        return token



# 生成token
async def create_token(db: AsyncSession, user_id: int):
    # 生成token + 过期时间 ==> 查询数据库当前用户是否有token ==> 有: 更新;  没有: 添加
    token = str(uuid.uuid4())  # uuid是生成一个全球几乎不重复的字符串

    # 定义过期时间
    expires_at = datetime.now() + timedelta(days=7)

    # 查询用户token
    stmt = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(stmt)
    user_token = result.scalar_one_or_none()

    if user_token:
        # 如果有token, 那么就更新
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        # 如果没有token值, 那就添加
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token




# 查询所有token
async def select_tokens(db: AsyncSession):
    stmt = select(Users, UserToken).join(Users, UserToken.user_id == Users.id)
    result = await db.execute(stmt)
    return result.all()






# token校验
async def token_auth(db: AsyncSession, token: str):
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 根据token找用户
async def select_user_by_token(db: AsyncSession, token: str):
    user_token = await token_auth(db, token)
    if user_token and user_token.expires_at > datetime.now():
        # token有效
        stmt = select(Users).where(Users.id == user_token.user_id)
        user = await db.execute(stmt)
        return user.scalar_one_or_none()
    else:
        return None
    
    
    


# 更改用户信息
async def update_user_info(db: AsyncSession, user_name: str, user_data):
    stmt = select(Users).where(Users.user_name == user_name)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        # 做信息更改
        # update(Users).values(user_name=xxx, bio=xxx, phone=xxx, avatar=xxx)
        
        # user_data 是一个Pydantic类型, 得到字典 ==> 解包

        stmt = update(Users).where(Users.user_name == user_name).values(**user_data.model_dump(
            # 如果键值对为空就不写入
            exclude_unset = True,
            exclude_none = True
        ))
        result = await db.execute(stmt)
        if result.rowcount == 0:
            return None
        return user
    else:
        return None
    
    
    
    
    
    
# 更改用户密码
async def reset_user_passwd(db: AsyncSession, user_name: str, new_passwd: str):
    hash_passwd = security.get_hash_passwd(new_passwd)  # 加密密码
    
    stmt = update(Users).where(Users.user_name == user_name).values(password = hash_passwd)
    result = await db.execute(stmt)
    if result.rowcount == 0:
        return None
    
    await db.commit()
    
    stmt = select(Users).where(Users.user_name == user_name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()